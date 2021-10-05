from .models import CallsOrder, DoctorsSchedule
from rest_framework import serializers
from ..profiles.models import DoctorsProfiles, PatientProfile


class CallsOrderSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField('get_doctor')

    class Meta:
        model = CallsOrder
        fields = '__all__'

    @staticmethod
    def get_doctor(obj):
        return DoctorsProfiles.objects.filter(user_id=obj.doctor_id).values()[0]


class ScheduledOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallsOrder
        fields = '__all__'


class DoctorsOrderSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField('get_patient')

    class Meta:
        model = CallsOrder
        fields = '__all__'

    @staticmethod
    def get_patient(obj):
        return PatientProfile.objects.filter(user_id=obj.patient_id).values()[0]


class DoctorsScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorsSchedule
        fields = '__all__'
