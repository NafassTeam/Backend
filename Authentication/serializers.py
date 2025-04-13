from rest_framework import serializers
from .models import User, Therapist, Patient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role', 'profile_picture', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TherapistSerializer(serializers.ModelSerializer):
    # User-related fields (flattened)
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    profile_picture = serializers.CharField(source='user.profile_picture', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Therapist
        fields = [
            # User fields (flat)
            'email', 'username', 'role',
            'profile_picture', 'first_name', 'last_name', 'phone_number',
            # Therapist-specific fields
            'bio', 'cv', 'cover_letter', 'recommendation_letter',
            'documents', 'status', 'interview_date'
        ]        
        
        
class TherapistCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)  # Consider using a proper registration flow
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True, required=False) # Make required=False if not always needed
    profile_picture = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = Therapist
        fields = [
            'email', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'role',
            'bio', 'cv', 'cover_letter', 'recommendation_letter',
            'documents', 'interview_date' # 'status' might be set server-side
        ]
        extra_kwargs = {'password': {'write_only': True}}        


    def create(self, validated_data):
        user_data = {
            'email': validated_data.pop('email'),
            'username': validated_data.pop('username'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'phone_number': validated_data.pop('phone_number', ''),
            'profile_picture': validated_data.pop('profile_picture', None),
            'role': validated_data.pop('role', 'therapist'),  # Default role
        }
        password = validated_data.pop('password')
        user = User.objects.create_user(**user_data, password=password)
        therapist = Therapist.objects.create(user=user, **validated_data)
        return therapist


class PatientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)
    profile_picture = serializers.CharField(write_only=True, required=False)
    phone_number = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Patient
        fields = [
            # user-related (flat)
            'email', 'username', 'password', 'role', 'profile_picture',
            'first_name', 'last_name', 'phone_number',
            # patient-specific
            'questionnaireResult', 'payment_method',
        ]

    def create(self, validated_data):
        user_data = {
            'email': validated_data.pop('email'),
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'role': validated_data.pop('role', 'patient'),
            'profile_picture': validated_data.pop('profile_picture', None),
            'phone_number': validated_data.pop('phone_number'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
        }

        if validated_data.get('payment_method') not in ['CCP', 'BaridiMob']:
            raise serializers.ValidationError("Invalid payment method. Allowed: 'CCP' or 'BaridiMob'.")

        user = User.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient
    