from rest_framework.serializers import ModelSerializer
from .models import (DoctorsProfiles, PatientProfile)


class DoctorProfileSerializer(ModelSerializer):

    class Meta:
        model = DoctorsProfiles
        fields = '__all__'


class PatientsProfileSerializer(ModelSerializer):

    class Meta:
        model = PatientProfile
        fields = '__all__'
