from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import OTP
import random

User = get_user_model()


class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, required=True)
    
    def validate_phone(self, value):
        # Check rate limiting
        one_hour_ago = timezone.now() - timedelta(hours=1)
        otp_requests = OTP.objects.filter(
            phone=value,
            created_at__gte=one_hour_ago
        ).count()
        
        max_attempts = settings.OTP_MAX_ATTEMPTS_PER_HOUR
        if otp_requests >= max_attempts:
            raise serializers.ValidationError(
                f'Too many OTP requests. Please try again after an hour.'
            )
        
        return value
    
    def create_otp(self):
        phone = self.validated_data['phone']
        
        # Generate OTP (in production, use random 6-digit)
        # For testing, using 123456
        otp_code = '123456'  # str(random.randint(100000, 999999))
        
        # Set expiry time
        validity_minutes = settings.OTP_VALIDITY_MINUTES
        expires_at = timezone.now() + timedelta(minutes=validity_minutes)
        
        # Create OTP record
        otp = OTP.objects.create(
            phone=phone,
            otp=otp_code,
            expires_at=expires_at
        )
        
        # In production, send OTP via SMS gateway here
        print(f"OTP for {phone}: {otp_code}")
        
        return otp_code


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, required=True)
    otp = serializers.CharField(max_length=6, required=True)
    
    def validate(self, data):
        phone = data['phone']
        otp_code = data['otp']
        
        try:
            # Get the latest OTP for this phone
            otp_record = OTP.objects.filter(
                phone=phone,
                is_used=False
            ).latest('created_at')
            
            # Check if OTP is expired
            if otp_record.is_expired():
                raise serializers.ValidationError('OTP has expired')
            
            # Check if OTP matches
            if otp_record.otp != otp_code:
                # Increment attempt count
                otp_record.attempt_count += 1
                otp_record.save()
                raise serializers.ValidationError('Invalid OTP')
            
            # Mark OTP as used
            otp_record.is_used = True
            otp_record.save()
            
            data['otp_record'] = otp_record
            return data
            
        except OTP.DoesNotExist:
            raise serializers.ValidationError('Invalid OTP or phone number')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'name', 'email', 'date_joined']
        read_only_fields = ['date_joined']

        