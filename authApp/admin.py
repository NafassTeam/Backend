from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Therapist, Patient, Match, Session

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
    
    
@admin.register(Therapist)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Therapist._meta.fields]
    
@admin.register(Patient)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Patient._meta.fields]
    
@admin.register(Match)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Match._meta.fields]

@admin.register(Session)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Session._meta.fields]
    list_filter = ['therapist', 'patient']