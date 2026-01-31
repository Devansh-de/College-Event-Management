from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from apps.events.models import Event
from apps.resources.models import Resource, Booking
from datetime import timedelta

class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        
        # Create resources
        self.room = Resource.objects.create(name="Conf Room A", resource_type=Resource.Type.ROOM)
        self.lab = Resource.objects.create(name="Lab 1", resource_type=Resource.Type.LAB)
        
        # Create events
        Event.objects.create(
            title="Event 1", 
            description="Desc", 
            start_time=timezone.now(), 
            end_time=timezone.now() + timedelta(hours=2),
            budget=1000.00
        )
        Event.objects.create(
            title="Event 2", 
            description="Desc", 
            start_time=timezone.now(), 
            end_time=timezone.now() + timedelta(hours=2),
            budget=500.50
        )
        
        # Create bookings
        Booking.objects.create(
            resource=self.room,
            user=self.user,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            status=Booking.Status.CONFIRMED
        )
        Booking.objects.create(
            resource=self.lab,
            user=self.user,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            status=Booking.Status.PENDING
        )

    def test_dashboard_context(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check Budget
        # 1000 + 500.50 = 1500.50
        self.assertEqual(float(response.context['total_budget']), 1500.50)
        
        # Check Bookings
        self.assertEqual(response.context['total_bookings'], 2)
        self.assertEqual(response.context['pending_bookings'], 1)
        self.assertEqual(response.context['confirmed_bookings'], 1)
        
        # Check Chart Data presence
        self.assertIn('bookings_chart_labels', response.context)
        self.assertIn('bookings_chart_data', response.context)
        
        # Check Resource Type counts in chart data
        # We have 1 booking for ROOM and 1 for LAB
        # The order in bookings_chart_data depends on default ordering/grouping, 
        # but the sum should be 2.
        self.assertEqual(sum(response.context['bookings_chart_data']), 2)

