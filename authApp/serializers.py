from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Therapist, Patient, Match, Session
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "birth_date",
            "gender",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        if self.instance and self.instance.email != value:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )
        return value


class TherapistCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    address = serializers.CharField(required=False)
    province = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    professional_title = serializers.CharField(required=False)
    degree = serializers.CharField(required=False)
    university = serializers.CharField(required=False)
    experience_years = serializers.IntegerField(required=True)
    languages_spoken = serializers.CharField(required=False)
    specialization = serializers.CharField(required=False)
    autorization_number = serializers.CharField(required=False)
    documents = serializers.FileField(required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "birth_date",
            "gender",
            "address",
            "province",
            "city",
            "professional_title",
            "degree",
            "university",
            "experience_years",
            "languages_spoken",
            "specialization",
            "autorization_number",
            "documents",
            "profile_picture",
        ]

    def create(self, validated_data):
        therapist_data = {
            "address": validated_data.pop("address", None),
            "province": validated_data.pop("province", None),
            "city": validated_data.pop("city", None),
            "professional_title": validated_data.pop("professional_title", None),
            "degree": validated_data.pop("degree", None),
            "university": validated_data.pop("university", None),
            "experience_years": validated_data.pop("experience_years", None),
            "languages_spoken": validated_data.pop("languages_spoken", None),
            "specialization": validated_data.pop("specialization", None),
            "autorization_number": validated_data.pop("autorization_number", None),
            "documents": validated_data.pop("documents", None),
        }
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data.get("phone_number"),
            birth_date=validated_data.get("birth_date"),
            gender=validated_data["gender"],
            profile_picture=validated_data.get("profile_picture"),
            role="therapist",  # Explicitly setting role
        )
        Therapist.objects.create(user=user, **therapist_data)
        return user


class PatientCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    profile_picture = serializers.ImageField(required=False)
    questionnaire_result = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_null=True, default=list
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "birth_date",
            "gender",
            "profile_picture",
            "questionnaire_result",
        ]

    def create(self, validated_data):
        questionnaire_result = validated_data.pop("questionnaire_result", [])
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data.get("phone_number"),
            birth_date=validated_data.get("birth_date"),
            gender=validated_data["gender"],
            profile_picture=validated_data.get("profile_picture"),
            role="patient",  # Explicitly setting role
        )
        Patient.objects.create(user=user, questionnaire_result=questionnaire_result)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Email and password are required.")
        return data


class TherapistSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    role = serializers.CharField(source="user.role")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Therapist
        fields = [
            "id",
            "email",
            "role",
            "first_name",
            "last_name",
            "address",
            "province",
            "city",
            "professional_title",
            "degree",
            "university",
            "experience_years",
            "languages_spoken",
            "specialization",
            "autorization_number",
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        # Separate out nested user data
        user_data = validated_data.pop("user", {})

        # Update Patient model fields dynamically
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related User model fields dynamically
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance


class PatientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    role = serializers.CharField(source="user.role")
    questionnaire_result = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_null=True
    )

    class Meta:
        model = Patient
        fields = [
            "id",
            "email",
            "role",
            "first_name",
            "last_name",
            "questionnaire_result",
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        questionnaire_result = validated_data.pop("questionnaire_result", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if questionnaire_result is not None:
            instance.questionnaire_result = questionnaire_result
        instance.save()
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        return instance


class MatchSerializer(serializers.ModelSerializer):
    patient_email = serializers.EmailField(source="patient.user.email", read_only=True)
    therapist_email = serializers.EmailField(
        source="therapist.user.email", read_only=True
    )
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source="patient"
    )
    therapist_id = serializers.PrimaryKeyRelatedField(
        queryset=Therapist.objects.all(), source="therapist"
    )

    class Meta:
        model = Match
        fields = [
            "id",
            "patient_id",
            "therapist_id",
            "patient_email",
            "therapist_email",
            "match_score",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "patient_email", "therapist_email"]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
        read_only_fields = ["id", "created_at"]
