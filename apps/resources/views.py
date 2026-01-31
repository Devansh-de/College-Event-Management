from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resource
from .forms import ResourceForm

@login_required
def resource_list(request):
    resources = Resource.objects.all()
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        resources = resources.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(resource_type__icontains=query)
        )
    return render(request, 'resources/venue_list.html', {'resources': resources, 'query': query})

@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/resource_detail.html', {'resource': resource})

@login_required
def resource_create(request):
    if not request.user.role == 'ADMIN':
        return redirect('resource_list')
    if request.method == "POST":
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'resources/resource_form.html', {'form': form, 'title': 'Add Venue'})

@login_required
def resource_update(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if not request.user.role == 'ADMIN':
        return redirect('resource_detail', pk=pk)
    if request.method == "POST":
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_detail', pk=pk)
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resources/resource_form.html', {'form': form, 'title': 'Edit Venue'})
