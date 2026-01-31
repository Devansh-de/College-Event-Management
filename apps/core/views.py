from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.events.models import Event
from apps.resources.models import Booking

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    from apps.events.models import Participant
    from django.db.models import Count
    from django.db.models.functions import ExtractMonth
    import json

    user = request.user
    
    # Statistics
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    upcoming_events_count = Event.objects.filter(status='UPCOMING').count()
    completed_events_count = Event.objects.filter(status='COMPLETED').count()
    
    # Budget Aggregation
    from django.db.models import Sum
    total_budget_agg = Event.objects.aggregate(Sum('budget'))
    total_budget = total_budget_agg['budget__sum'] or 0.00

    # Chart Data: Events per month
    events_per_month = Event.objects.annotate(month=ExtractMonth('start_time')).values('month').annotate(count=Count('id')).order_by('month')
    
    # Fill in months with zero if no events
    months_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    chart_data = [0] * 12
    for entry in events_per_month:
        if entry['month']:
            chart_data[entry['month']-1] = entry['count']

    # Bookings Statistics
    from apps.resources.models import Booking
    from apps.communities.models import Club
    
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
    
    # Clubs Statistics
    total_clubs = Club.objects.filter(is_active=True).count()
    
    # Chart Data: Bookings per Resource Type
    from apps.resources.models import Resource
    resource_type_counts = Resource.objects.annotate(total_bookings=Count('bookings')).values('resource_type', 'total_bookings')
    
    bookings_chart_labels = []
    bookings_chart_data = []
    
    # Mapping for display names if needed, or just use the code
    type_display_map = dict(Resource.Type.choices)

    for entry in resource_type_counts:
        # Get display name or raw type
        rtype = entry['resource_type']
        label = type_display_map.get(rtype, rtype)
        bookings_chart_labels.append(label)
        bookings_chart_data.append(entry['total_bookings'])
    
    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events_count': upcoming_events_count,
        'completed_events_count': completed_events_count,
        'total_budget': total_budget,
        
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_clubs': total_clubs,
        
        'chart_labels': months_labels,
        'chart_data': chart_data,
        
        'bookings_chart_labels': bookings_chart_labels,
        'bookings_chart_data': bookings_chart_data,
        
        'bookings_chart_data': bookings_chart_data,
        
        'recent_events': Event.objects.order_by('-created_at')[:5],
        'memberships': user.club_memberships.select_related('club').all() if user.is_authenticated else []
    }

    
    return render(request, 'core/dashboard.html', context)


@login_required
def reports(request):
    events = Event.objects.all()
    
    # Filter by status
    status = request.GET.get('status')
    if status and status != 'all':
        events = events.filter(status=status.upper())
    
    # Filter by date
    date = request.GET.get('date')
    if date:
        from datetime import datetime
        try:
            filter_date = datetime.strptime(date, '%Y-%m-%d')
            events = events.filter(start_time__year=filter_date.year, start_time__month=filter_date.month)
        except ValueError:
            pass
    
    return render(request, 'core/reports.html', {'events': events})


@login_required
def export_reports_csv(request):
    import csv
    from django.http import HttpResponse
    
    events = Event.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="events_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Status', 'Start Time', 'End Time', 'Budget'])
    
    for event in events:
        writer.writerow([event.title, event.status, event.start_time, event.end_time, event.budget])
        
    return response

@login_required
def export_reports_excel(request):
    # For a hackathon, we can use a CSV with .xls extension if openpyxl isn't available, 
    # but let's try to stick to standard CSV or inform if lib is missing.
    return export_reports_csv(request) # Simple fallback
