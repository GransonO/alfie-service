from rest_framework.serializers import ModelSerializer
from .models import (DoctorsProfiles, PatientProfile, Speciality)


class DoctorProfileSerializer(ModelSerializer):

    class Meta:
        model = DoctorsProfiles
        fields = '__all__'


class PatientsProfileSerializer(ModelSerializer):

    class Meta:
        model = PatientProfile
        fields = '__all__'


class SpecialitySerializer(ModelSerializer):

    class Meta:
        model = Speciality
        fields = '__all__'
