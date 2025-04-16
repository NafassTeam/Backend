from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    MALE='M'
    FEMALE='F'
    
    
    
    GENDER_CHOICES=[
        (MALE,'Male'),
        (FEMALE,'Female'),
    ]

    #role = models.CharField(max_length=20, choices=[('patient', 'Patient'), ('therapist', 'Therapist'), ('admin', 'Admin')], default='patient')  # User role
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )  # URL to the profile picture
    first_name = models.CharField(max_length=150)  # Required
    last_name = models.CharField(max_length=150)   # Required
    phone_number = models.CharField(
    max_length=13,
    blank=True,
    null=True,
    validators=[
        RegexValidator(
            regex=r'^\+213[5-7]\d{8}$',
            message="Enter a valid Algerian phone number (e.g., +213661234567)."
        )
    ]
    )
    
    birth_date = models.DateField(null=True, blank=True)  # Therapist's birth date
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES)


    

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'  # Use email instead of username for authentication
    REQUIRED_FIELDS = ['username','first_name','last_name']  # Fields required when creating a superuser (besides email)
    

    
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patients")  # One-to-one relationship with User
    
class Therapist(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="therapists")  # One-to-one relationship with User
    address= models.CharField(max_length=255, blank=True, null=True)  # Therapist's address
    province= models.CharField(max_length=255, blank=True, null=True)  # Therapist's province
    city= models.CharField(max_length=255, blank=True, null=True)  # Therapist's city
    professional_title= models.CharField(max_length=255, blank=True, null=True)  # Therapist's professional title
    degree= models.CharField(max_length=255, blank=True, null=True)  # Therapist's degree
    university= models.CharField(max_length=255, blank=True, null=True)  # Therapist's university
    experience_years= models.PositiveIntegerField(blank=True, null=True)  # Therapist's years of experience
    languages_spoken= models.CharField(max_length=255, blank=True, null=True)  # Languages spoken by the therapist
    specialization= models.CharField(max_length=255, blank=True, null=True)  # Therapist's specialties
    autorization_number= models.CharField(max_length=255, blank=True, null=True)  # Therapist's authorization number
    documents = models.FileField(
        upload_to='therapist_docs/',
        blank=True,
        null=True,
    )
    