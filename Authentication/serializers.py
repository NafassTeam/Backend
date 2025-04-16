from rest_framework import serializers
from .models import User, Therapist, Patient
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username', 'password', 'profile_picture', 'first_name', 'last_name', 'phone_number','birth_date','gender']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def validate_email(self, value):
        if self.instance and self.instance.email != value:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email format.")
        return value
    
    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        return value


class TherapistCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    profile_picture = serializers.ImageField(required=False)
    documents = serializers.FileField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'birth_date', 'gender',
            'profile_picture', 'address', 'province', 'city', 'professional_title', 'degree', 'university',
            'experience_years', 'languages_spoken', 'specialization', 'autorization_number', 'documents'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'gender': {'required': True},
            'specialization': {'required': True},
            'autorization_number': {'required': True},
        }
    def create(self, validated_data):
        therapist_data = {
            'address': validated_data.pop('address', None),
            'province': validated_data.pop('province', None),
            'city': validated_data.pop('city', None),
            'professional_title': validated_data.pop('professional_title', None),
            'degree': validated_data.pop('degree', None),
            'university': validated_data.pop('university', None),
            'experience_years': validated_data.pop('experience_years', None),
            'languages_spoken': validated_data.pop('languages_spoken', None),
            'specialization': validated_data.pop('specialization'),
            'autorization_number': validated_data.pop('autorization_number'),
            'documents': validated_data.pop('documents', None),
        }
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            birth_date=validated_data.get('birth_date'),
            gender=validated_data['gender'],
            profile_picture=validated_data.get('profile_picture'),
        )
        Therapist.objects.create(user=user, **therapist_data)
        return user


class PatientCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'birth_date', 'gender', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'gender': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            birth_date=validated_data.get('birth_date'),
            gender=validated_data['gender'],
            profile_picture=validated_data.get('profile_picture'),
        )
        Patient.objects.create(user=user)
        return user
    