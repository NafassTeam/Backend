from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    role = models.CharField(max_length=20, choices=[('patient', 'Patient'), ('therapist', 'Therapist'), ('admin', 'Admin')], default='patient')  # User role
    is_verified = models.BooleanField(default=False)  # Whether the user is verified
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update
    profile_picture = models.CharField(max_length=255, blank=True, null=True)  # URL to the profile picture
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Phone number of the user

    USERNAME_FIELD = 'email'  # Use email instead of username for authentication
    REQUIRED_FIELDS = ['username']  # Fields required when creating a superuser (besides email)
    
    
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    questionnaireResult = models.JSONField(blank=True, null=True)  # Store questionnaire results as JSON
    recomnended_therapist = models.ForeignKey('Therapist', on_delete=models.SET_NULL, null=True, blank=True, related_name='recommended_patients')  # Recommended therapist for the patient
    selected_therapists = models.ManyToManyField('Therapist', related_name='selected_by', null=True, blank=True)  # Therapists selected by the patient
    payment_method = models.CharField(max_length=20, choices=[('CCP', 'CCP'), ('BARIDIMOB', 'BaridiMob')], null=True)

class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv = models.CharField(max_length=255, blank=True, null=True)  # URL to the CV
    cover_letter = models.CharField(max_length=255, blank=True, null=True)  # URL to the cover letter
    recommendation_letter = models.CharField(max_length=255, blank=True, null=True)  # URL to the recommendation letter
    documents = models.CharField(max_length=255, blank=True, null=True)  # URL to other documents
    profile_picture = models.CharField(max_length=255, blank=True, null=True)  # URL to the profile picture
    bio = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('interview', 'Interview'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')  # Application status
    interview_date = models.DateTimeField(null=True, blank=True)
