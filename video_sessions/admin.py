from django.contrib import admin
from .models import VideoSession


@admin.register(VideoSession)
class VideoSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "therapist",
        "patient",
        "room_id",
        "created_at",
        "is_active",
        "email_sent",
    )
    list_filter = ("is_active", "email_sent", "created_at")
    search_fields = ("room_id", "therapist__user__email", "patient__user__email")


# Register your models here.
