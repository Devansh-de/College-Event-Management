from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Event, Participant
from apps.resources.models import Resource
from .serializers import EventSerializer, ParticipantSerializer, UserSerializer, ResourceSerializer
from .forms import EventForm

# --- Template Views ---

@login_required
def event_list(request):
    events = Event.objects.all().order_by('-start_time')
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(venue__name__icontains=query) |
            Q(organizer__username__icontains=query)
        )
    return render(request, 'events/event_list.html', {'events': events, 'query': query})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Edit Event'})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def participant_list(request):
    participants = Participant.objects.all().select_related('user', 'event')
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        participants = participants.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query) |
            Q(roll_no__icontains=query) |
            Q(event__title__icontains=query)
        )
    return render(request, 'events/participants.html', {'participants': participants})

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.role == 'STUDENT':
        Participant.objects.get_or_create(user=request.user, event=event)
        return redirect('event_detail', pk=pk)
    return redirect('event_list')

@login_required
def event_approve(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('event_list')
    event = get_object_or_404(Event, pk=pk)
    event.status = 'UPCOMING'
    event.save()
    return redirect('event_list')

@login_required
def event_reject(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('event_list')
    event = get_object_or_404(Event, pk=pk)
    event.status = 'REJECTED'
    event.save()
    return redirect('event_list')

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if request.user.role != 'ADMIN':
            return Response({'error': 'Only admins can approve events'}, status=status.HTTP_403_FORBIDDEN)
        event = self.get_object()
        event.status = 'UPCOMING'
        event.save()
        return Response({'status': 'event approved'})

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def register(self, request):
        event_id = request.data.get('event_id')
        try:
            event = Event.objects.get(id=event_id)
            participant, created = Participant.objects.get_or_create(
                user=request.user,
                event=event
            )
            if not created:
                return Response({'error': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'registered successfully'})
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
