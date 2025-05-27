from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid


class User(AbstractUser):

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    ROLES_CHOICES = [
        ("patient", "patient"),
        ("therapist", "therapist"),
        ("admin", "admin"),
    ]

    role = models.CharField(
        max_length=20, choices=ROLES_CHOICES, null=False
    )  # User role
    email = models.EmailField(
        unique=True, blank=False, null=False
    )  # User email (unique)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )  # URL to the profile picture
    first_name = models.CharField(max_length=150)  # Required
    last_name = models.CharField(max_length=150)  # Required
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^\+213[5-7]\d{8}$",
                message="Enter a valid Algerian phone number (e.g., +213661234567).",
            )
        ],
    )

    birth_date = models.DateField(null=True, blank=True)  # Therapist's birth date
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_verified = models.BooleanField(default=False)  # Verification status
    email_verification_token = models.UUIDField(
        default=uuid.uuid4, null=True, blank=True
    )

    def __str__(self):
        return self.username

    USERNAME_FIELD = "email"  # Use email instead of username for authentication
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]  # Fields required when creating a superuser (besides email)


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patients"
    )  # One-to-one relationship with User
    questionnaire_result = models.JSONField(
        blank=True,
        null=True,
        default=list,
        help_text="Stores an array of integers for questionnaire results.",
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Patient)"


class Therapist(models.Model):
    # should add a dropdown list for the most of the coming attributes:
    # recontruct the address attribute to be made of many other attributes like province, city, etc.

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="therapists"
    )  # One-to-one relationship with User
    address = models.CharField(
        max_length=255, blank=True, null=True
    )  # Therapist's address
    province = models.CharField(
        max_length=255, blank=True, null=True
    )  # Therapist's province
    city = models.CharField(max_length=255, blank=True, null=True)  # Therapist's city
    professional_title = models.CharField(
        max_length=255, blank=True, null=True
    )  # Therapist's professional title
    degree = models.CharField(
        max_length=255, blank=True, null=True
    )  # Therapist's degree
    university = models.CharField(
        max_length=255, blank=True, null=True
    )  # Therapist's university
    experience_years = models.PositiveIntegerField()  # Therapist's years of experience
    languages_spoken = models.CharField(
        max_length=255, blank=True, null=True
    )  # Languages spoken by the therapist
    specialization = models.CharField(
        max_length=255, blank=True, null=True
    )  # Therapist's specialties
    autorization_number = models.CharField(
        max_length=255, blank=True, null=True
    )  # Therapist's authorization number
    documents = models.FileField(upload_to="therapist_docs/", blank=True, null=True)
    cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )  # Cost of therapy sessions
    features = models.JSONField(
        blank=True,
        null=True,
        default=list,
        help_text="Stores an array of integers for therapist features.",
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Therapist)"


# this is the model that will be used to store the matches between patients and therapists
class Match(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="matches"
    )
    therapist = models.ForeignKey(
        Therapist, on_delete=models.CASCADE, related_name="matches"
    )
    # status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    match_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.username} ↔ {self.therapist.user.username} ({self.match_score})"


class Session(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="sessions"
    )
    therapist = models.ForeignKey(
        Therapist, on_delete=models.CASCADE, related_name="sessions"
    )
    scheduled_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    session_type = models.CharField(
        max_length=20,
        choices=[("video", "Video"), ("chat", "Chat"), ("phone", "Phone")],
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.patient.user.username} with {self.therapist.user.username}"
