from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from core.models import ServiceCategory, Service, Appointment, Review

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(validators = [UniqueValidator(queryset=User.objects.all(), message="Username already exists.")])
    email = serializers.EmailField(validators = [UniqueValidator(queryset=User.objects.all(), message="Username already exists.")])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    # This is NOT a model field; we use it only in serializer logic
    role = serializers.ChoiceField(
        choices=[('customer', 'Customer'), ('provider', 'Provider')],
        write_only=True
    )
    full_name = serializers.CharField(write_only = True)
    phone = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)

    def create(self, validated_data):
        role = validated_data.pop('role')  # remove from validated_data so it's not passed to create_user()
        full_name = validated_data.pop('full_name')
        phone = validated_data.pop('phone')
        address = validated_data.pop('address')
        location = validated_data.pop('location')

        user = User.objects.create_user(**validated_data)

        if role == 'customer':
            user.is_customer = True
        elif role == 'provider':
            user.is_service_provider = True
        user.save()

        Profile.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            address=address,
            location=location
        )

        return user
    
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    provider = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['provider']

class AppointmentSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only = True)
    provider = serializers.StringRelatedField(read_only = True)
    

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['customer', 'provider', 'status', 'is_confirmed']

class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only = True)
    provider = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['customer', 'provider']