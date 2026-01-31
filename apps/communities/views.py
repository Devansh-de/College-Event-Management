from django.shortcuts import render, get_object_or_404
from .models import Club

def club_list(request):
    clubs = [
        {'id': 1, 'name': 'Tech Club', 'description': 'Innovating the future', 'is_active': True, 'image': 'images/tech_club.png'},
        {'id': 2, 'name': 'Dance Club', 'description': 'Express yourself through movement', 'is_active': True, 'image': 'images/dance_club.png'},
        {'id': 3, 'name': 'Art Society', 'description': 'Creativity without limits', 'is_active': True, 'image': 'images/art_society.png'},
    ]
    return render(request, 'communities/club_list.html', {'clubs': clubs})

def club_detail(request, club_id):
    clubs = [
        {'id': 1, 'name': 'Tech Club', 'description': 'Innovating the future', 'is_active': True, 'image': 'images/tech_club.png'},
        {'id': 2, 'name': 'Dance Club', 'description': 'Express yourself through movement', 'is_active': True, 'image': 'images/dance_club.png'},
        {'id': 3, 'name': 'Art Society', 'description': 'Creativity without limits', 'is_active': True, 'image': 'images/art_society.png'},
    ]
    club = next((c for c in clubs if c['id'] == int(club_id)), clubs[0])
    return render(request, 'communities/club_detail.html', {'club': club})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Club, Membership

@login_required
def join_club(request, club_id):
    if request.method == 'POST':
        try:
            club = Club.objects.get(id=club_id, is_active=True)
            # Check if already a member
            existing = Membership.objects.filter(user=request.user, club=club).first()
            if existing:
                messages.info(request, f"You are already a member of {club.name}!")
            else:
                Membership.objects.create(user=request.user, club=club, role='MEMBER')
                messages.success(request, f"Successfully joined {club.name}!")
        except Club.DoesNotExist:
            messages.error(request, "Club not found.")
    return redirect('club_detail', club_id=club_id)
