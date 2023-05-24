from rest_framework import serializers, status
from django.contrib.auth.password_validation import ValidationError
from .models import Student, Sponsor, Metsenat


class SponsorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('full_name', 'phone_number', 'sponsor_type', 'payment_amount', 'organization_name')

    def validate(self, attrs):
        organization_name=attrs.get('organization_name')
        sponsor_type=attrs.get('sponsor_type')
        if sponsor_type=="LEGAL_ENTITY" and not organization_name:
            raise ValidationError({
                "success": False,
                "message": "Tashkilot nomini kiriting"
            }, status.HTTP_400_BAD_REQUEST)
        return attrs


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = (
            'id',
            'full_name',
            'phone_number',
            'sponsor_type',
            'organization_name',
            'payment_type',
            'payment_amount',
            'amount_spent',
            'created_at',
            'status'
        )
        extra_kwargs = {
            'full_name': {'read_only': True, 'required': False},
            'phone_number': {'read_only': True, 'required': False},
            'sponsor_type': {'read_only': True, 'required': False},
            'organization_name': {'read_only': True, 'required': False},
            'amount_spent': {'read_only': True, 'required': False},
            'created_at': {'read_only': True, 'required': False}
        }


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id',
            'full_name',
            'phone_number',
            'degree_type',
            'university_name',
            'amount_spent',
            'payment_amount',
            'created_at'
        )
        extra_kwargs = {
            'amount_spent': {'read_only': True, 'required': False},
            'created_at': {'read_only': True, 'required': False}
        }


class MetsenatSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Metsenat
        fields = ('sponsor', 'sponsor_id', 'student_id', 'money', 'created_at')

    @staticmethod
    def validate_money(attrs):
        if attrs<50000:
            raise ValidationError(
               "Kechirasiz, minimal miqdor 50 000 ming so'm"
            )
