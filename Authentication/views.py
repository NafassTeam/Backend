from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Therapist, Patient
from .serializers import UserSerializer, TherapistSerializer, PatientSerializer, TherapistCreateSerializer


class IndexView(APIView):
    def get(self, request):
        return Response(
            {"message": "Hello, world. You're at the authentication index."}
        )


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully", "user_id": user.id}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTherapistView(APIView):
    def post(self, request):
        serializer = TherapistCreateSerializer(data=request.data)
        if serializer.is_valid():
            therapist = serializer.save()
            return Response(
                {
                    "message": "Therapist created successfully",
                    "therapist_id": therapist.id,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePatientView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            return Response(
                {"message": "Patient created successfully", "patient_id": patient.id}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPatientView(APIView):
    def get(self, request, user_id):
        try:
            patient = Patient.objects.select_related("user").get(user__id=user_id)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND
            )


class GetTherapistView(APIView):
    def get(self, request, user_id):
        try:
            therapist = Therapist.objects.select_related("user").get(user__id=user_id)
            serializer = TherapistSerializer(therapist)
            return Response(serializer.data)
        except Therapist.DoesNotExist:
            return Response(
                {"error": "Therapist not found."}, status=status.HTTP_404_NOT_FOUND
            )


class GetUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class UpdateUserView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class DeleteUserView(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully"})
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class TherapistListView(APIView):
    def get(self, request):
        therapists = Therapist.objects.all()
        serializer = TherapistSerializer(therapists, many=True)
        return Response(serializer.data)


class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class TherapistUpdateView(APIView):
    def put(self, request, user_id):
        try:
            therapist = Therapist.objects.get(user__id=user_id)
            serializer = TherapistSerializer(therapist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Therapist updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Therapist.DoesNotExist:
            return Response(
                {"error": "Therapist not found."}, status=status.HTTP_404_NOT_FOUND
            )


class PatientUpdateView(APIView):
    def put(self, request, user_id):
        try:
            patient = Patient.objects.get(user__id=user_id)
            serializer = PatientSerializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Patient updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND
            )


class TherapistDeleteView(APIView):
    def delete(self, request, user_id):
        try:
            therapist = Therapist.objects.get(user__id=user_id)
            therapist.delete()
            return Response({"message": "Therapist deleted successfully"})
        except Therapist.DoesNotExist:
            return Response(
                {"error": "Therapist not found."}, status=status.HTTP_404_NOT_FOUND
            )


class PatientDeleteView(APIView):
    def delete(self, request, user_id):
        try:
            patient = Patient.objects.get(user__id=user_id)
            patient.delete()
            return Response({"message": "Patient deleted successfully"})
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND
            )
