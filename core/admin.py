from django.contrib import admin
from core.models import User, Profile, ServiceCategory, Service, Appointment, Review
# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(Review)