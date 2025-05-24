from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from core.serializers import RegisterSerializer, ServiceCategorySerializer, ServiceSerializer, AppointmentSerializer, ReviewSerializer
from rest_framework.permissions import AllowAny
from core.models import User, Profile, ServiceCategory, Service, Appointment, Review
from rest_framework import viewsets, permissions
from core.permissions import IsServiceProvider
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from twilio.rest import Client

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(provider = self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsServiceProvider()]
        return [permissions.AllowAny()]
    
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']
        provider = service.provider

        if Appointment.objects.filter(provider=provider, date=date, time=time).exists():
            raise ValidationError("Provider already booked at this time.")
        
        if self.request.user.is_staff:
            status = "approved"
            is_confirmed = True
        else:
            status = "pending"
            is_confirmed = False

        serializer.save(
            customer=self.request.user,
            provider=provider,
            status=status,
            is_confirmed=is_confirmed
        )

        # serializer.save(
        #         customer = self.request.user,
        #         provider = provider,
        #         status = "pending",
        #         is_confirmed = False
        #     )
        
        send_mail(
            subject="new appointement Requested",
            message=f"You have a new appointment request from {self.request.user.username}",
            from_email="noreply@localservicebooking.com",
            recipient_list=[provider.email],
            fail_silently=True,
        )
    @action(detail=False, methods=['get'], url_path='available-slots')
    def available_slots(self, request):
        service_id = request.query_params.get('service_id')
        date_str = request.query_params.get('date')  # Format: YYYY-MM-DD

        if not service_id or not date_str:
            return Response({"error": "service_id and date are required"}, status=400)

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        service = get_object_or_404(Service, id=service_id)
        provider = service.provider

        all_slots = [datetime.strptime(f"{hour}:00", "%H:%M").time() for hour in range(9, 18)]
        booked_slots = Appointment.objects.filter(provider=provider, date=date).values_list('time', flat=True)
        available_slots = [slot.strftime("%H:%M") for slot in all_slots if slot not in booked_slots]

        return Response({"available_slots": available_slots})
    

    def send_sms(to_number, message):
        account_sid = 'your_sid'
        auth_token = 'your_token'
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_='your_twilio_number',
            to=to_number
        )

    # Replace send_mail in `perform_create` with:
    # send_sms(
    #     to_number=self.provider.phone,  # Ensure you have this in your model
    #     message=f"You have a new appointment request from {self.request.user.username}"
    # )

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(customer=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        appointment = serializer.validated_date['appointment']

        if appointment.customer != self.request.user:
            raise ValidationError("You are not allowed to review this appointment.")
        
        if Review.objects.filter(appointment=appointment).exists():
            raise ValidationError("Review already submitted for this appointment.")
        
        serializer.save(
            customer = self.request.user,
            provider = appointment.provider
        )