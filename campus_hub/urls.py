from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.events.views import EventViewSet, ParticipantViewSet, UserViewSet, ResourceViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'venues', ResourceViewSet)

urlpatterns = [
    path('admin/', admin.path if hasattr(admin, 'path') else admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('events/', include('apps.events.urls')),
    path('resources/', include('apps.resources.urls')),
    path('communities/', include('apps.communities.urls')),
]

