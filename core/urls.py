from django.urls import path
from core.views import RegisterView, ServiceViewSet, ServiceCategoryViewSet, AppointmentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('service', ServiceViewSet)
router.register('categories', ServiceCategoryViewSet)
router.register('appointments', AppointmentViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
urlpatterns = router.urls