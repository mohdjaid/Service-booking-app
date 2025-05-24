from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)

    def __str__(self):
        return self.username
   
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
    
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_service_provider': True})
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.provider.username}"
    
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment', limit_choices_to={'is_customer':True})
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_appointment', limit_choices_to={'is_service_provider': True})
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('provider', 'date', 'time') #prevent double-booking...
    
    def __str__(self):
        return f"{self.customer.username} -> {self.provider.username} on {self.date} at {self.time}"

class Review(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_given')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_received')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) 
    commnet = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} -> {self.provider.username} | {self.rating}"