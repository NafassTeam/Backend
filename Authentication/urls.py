from django.urls import path
from .views import (
    IndexView,
    CreateUserView,
    CreateTherapistView,
    CreatePatientView,
    GetPatientView,
    GetTherapistView,
    GetUserView,
    UpdateUserView,
    DeleteUserView,
    TherapistListView,
    PatientListView,
    UserListView,
    TherapistUpdateView,
    PatientUpdateView,
    TherapistDeleteView,
    PatientDeleteView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create_user/", CreateUserView.as_view(), name="create_user"),
    path("create_therapist/", CreateTherapistView.as_view(), name="create_therapist"),
    path("create_patient/", CreatePatientView.as_view(), name="create_patient"),
    path("get_patient/<int:user_id>/", GetPatientView.as_view(), name="get_patient"),
    path(
        "get_therapist/<int:user_id>/", GetTherapistView.as_view(), name="get_therapist"
    ),
    path("get_user/<int:user_id>/", GetUserView.as_view(), name="get_user"),
    path("update_user/<int:user_id>/", UpdateUserView.as_view(), name="update_user"),
    path("delete_user/<int:user_id>/", DeleteUserView.as_view(), name="delete_user"),
    path("therapists/", TherapistListView.as_view(), name="therapist_list"),
    path("patients/", PatientListView.as_view(), name="patient_list"),
    path("users/", UserListView.as_view(), name="user_list"),
    path(
        "update_therapist/<int:user_id>/",
        TherapistUpdateView.as_view(),
        name="update_therapist",
    ),
    path(
        "update_patient/<int:user_id>/",
        PatientUpdateView.as_view(),
        name="update_patient",
    ),
    path(
        "delete_therapist/<int:user_id>/",
        TherapistDeleteView.as_view(),
        name="delete_therapist",
    ),
    path(
        "delete_patient/<int:user_id>/",
        PatientDeleteView.as_view(),
        name="delete_patient",
    ),
]
