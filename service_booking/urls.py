"""
URL configuration for service_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from core.views import RegisterView, ServiceViewSet, ServiceCategoryViewSet, AppointmentViewSet, ReviewViewSet
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('service', ServiceViewSet)
# router.register('categories', ServiceCategoryViewSet)
# router.register('appointments', AppointmentViewSet)
# router.register('reviews', ReviewViewSet)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('api/register/', RegisterView.as_view(), name='register'),
#     path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]

from django.contrib import admin
from django.urls import path, include
from core.views import RegisterView, ServiceViewSet, ServiceCategoryViewSet, AppointmentViewSet, ReviewViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

# DRF router for viewsets
router = DefaultRouter()
router.register('service', ServiceViewSet)
router.register('categories', ServiceCategoryViewSet)
router.register('appointments', AppointmentViewSet)
router.register('reviews', ReviewViewSet)

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # All ViewSets will be under /api/
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
