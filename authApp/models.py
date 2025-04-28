from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):

    GENDER_CHOICES=[
        ('M','Male'),
        ('F','Female'),
    ]
    ROLES_CHOICES=[
        ('patient','patient'),
        ('therapist','therapist'),
        ('admin','admin'),]

    role = models.CharField(max_length=20, choices=ROLES_CHOICES, null=False)  # User role
    email = models.EmailField(unique=True,blank=False,null=False)  # User email (unique)
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
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Patient)"
    
class Therapist(models.Model):
    #should add a dropdown list for the most of the coming attributes:
    #recontruct the address attribute to be made of many other attributes like province, city, etc.
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="therapists")  # One-to-one relationship with User
    address= models.CharField(max_length=255)  # Therapist's address
    province= models.CharField(max_length=255)  # Therapist's province
    city= models.CharField(max_length=255)  # Therapist's city
    professional_title= models.CharField(max_length=255)  # Therapist's professional title
    degree= models.CharField(max_length=255)  # Therapist's degree
    university= models.CharField(max_length=255)  # Therapist's university
    experience_years= models.PositiveIntegerField()  # Therapist's years of experience
    languages_spoken= models.CharField(max_length=255)  # Languages spoken by the therapist
    specialization= models.CharField(max_length=255)  # Therapist's specialties
    autorization_number= models.CharField(max_length=255)  # Therapist's authorization number
    documents = models.FileField(
        upload_to='therapist_docs/',
    )
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Therapist)"
    