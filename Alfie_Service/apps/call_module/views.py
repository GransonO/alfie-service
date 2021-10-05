import os
import uuid
import bugsnag
import time
from dotenv import load_dotenv

from .agora.RtcTokenBuilder import RtcTokenBuilder, Role_Publisher, Role_Subscriber
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import CallsOrderSerializer, DoctorsOrderSerializer, DoctorsScheduleSerializer, ScheduledOrderSerializer
from .models import CallsOrder, DoctorsSchedule
from ..profiles.models import PatientProfile, DoctorsProfiles
from ..profiles.serializers import PatientsProfileSerializer, DoctorProfileSerializer
from ..notifiers.FCM.fcm_requester import FcmRequester
from ..notifiers.EMAILS.mail_sender import SendMail


class DoctorRequest(views.APIView):
    """ Add a request to the therapist"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data
        try:
            the_id = uuid.uuid1()
            serializer = CallsOrderSerializer(
                data=passed_data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(session_id=the_id)
            # Notify therapist

            # *** Move this section to background
            # send FCM TO ALL SUBSCRIBERS
            patient = PatientProfile.objects.get(user_id=passed_data["patient_id"])
            patient_profile = PatientsProfileSerializer(patient).data
            doctor = DoctorsProfiles.objects.get(user_id=passed_data["doctor_id"])
            doctors_profile = DoctorProfileSerializer(doctor).data

            SendMail.send_doctor_request_email(
                email=doctors_profile["email"],
                patient_name=patient_profile["fullname"],
                session_id=str(the_id)
            )
            FcmRequester.doctor_call_notice(
                all_tokens=[doctors_profile["fcm"]],
                message="You have an new therapy request",
                user_id=passed_data["patient_id"],
                session_id=str(the_id)
            )
            # *** Move this section to background

            return Response(
                {
                    "success": True,
                    "message": "Posted successfully"
                }, status.HTTP_200_OK
            )
        except Exception as E:
            print("----------------------{}".format(E))
            bugsnag.notify(
                Exception('TherapistRequest Post: {}'.format(E))
            )
            return Response(
                {
                    "success": False,
                    "message": "Posting failed"
                }, status.HTTP_200_OK
            )

    @staticmethod
    def put(request):
        try:
            passed_data = request.data
            session = CallsOrder.objects.get(session_id=passed_data["session_id"])
            serializer = CallsOrderSerializer(
                session, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            session = CallsOrder.objects.get(session_id=passed_data["session_id"])
            serialized_session = CallsOrderSerializer(session).data
            patient = PatientProfile.objects.get(user_id=serialized_session["patient_id"])
            patient_profile = PatientsProfileSerializer(patient).data

            FcmRequester.call_notice(
                all_tokens=[patient_profile["fcm"]],
                message="Your request has been updated",
                doctor_id=serialized_session["doctor_id"],
                session_id=passed_data["session_id"]
            )

            return Response(
                {
                    "success": True,
                    "message": "Posted successfully"
                }, status.HTTP_200_OK
            )
        except Exception as E:
            print("-----------------Error---------------- : {}".format(E))
            # bugsnag.notify(
            #     Exception('TherapistRequest Post: {}'.format(E))
            # )
            return Response(
                {
                    "success": False,
                    "message": "Posting failed"
                }, status.HTTP_200_OK
            )


class TimeSchedule(views.APIView):
    permission_classes = [AllowAny]
    """Create a doctors weekly schedule"""
    @staticmethod
    def post(request):
        try:
            passed_data = request.data
            schedule_exists = DoctorsSchedule.objects.filter(doctor_id=passed_data["doctor_id"]).exists()
            if schedule_exists:
                # Update schedule
                schedule = DoctorsSchedule.objects.get(doctor_id=passed_data["doctor_id"])
                serializer = DoctorsScheduleSerializer(
                    schedule, data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                # Create new entry
                serializer = DoctorsScheduleSerializer(
                    data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Schedule created successfully"
                }, status.HTTP_200_OK
            )
        except Exception as E:
            print("-----------------Error---------------- : {}".format(E))
            bugsnag.notify(
                Exception('TherapistSchedule Post: {}'.format(E))
            )
            return Response(
                {
                    "success": False,
                    "message": "Posting failed"
                }, status.HTTP_200_OK
            )


class GetDoctorsSchedule(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorsScheduleSerializer

    def get_queryset(self):
        return DoctorsSchedule.objects.filter(
            doctor_id=self.kwargs['doctor_id']
            )


class GetUserRequests(generics.ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = CallsOrderSerializer

    def get_queryset(self):
        return CallsOrder.objects.filter(
            patient_id=self.kwargs['patient_id'],
            )


class GetDoctorsDateRequests(generics.ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = ScheduledOrderSerializer

    def get_queryset(self):
        return CallsOrder.objects.filter(
            doctor_id=self.kwargs['doctor_id'],
            scheduled_date=self.kwargs['scheduled_date'],
            )


class GetTherapistRequests(generics.ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = DoctorsOrderSerializer

    def get_queryset(self):
        return CallsOrder.objects.filter(
            doctor_id=self.kwargs['doctor_id']
            )


class SpecificRequest(generics.ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = CallsOrderSerializer

    def get_queryset(self):
        return CallsOrder.objects.filter(
            session_id=self.kwargs['session_id']
            ).order_by('createdAt')


class TokenGenerator(views.APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data

        load_dotenv()
        app_id = os.environ['ALFIE_AGORA_APP_ID']
        app_certificate = os.environ['ALFIE_AGORA_APP_CERTIFICATE']
        channel_name = passed_data["channel_name"]
        user_account = passed_data["callUid"]
        expire_time_in_seconds = 7200
        current_timestamp = int(time.time())
        privilege_expired_ts = current_timestamp + expire_time_in_seconds

        print("-------------- app_id ---------------- {}".format(app_id))
        print("-------------- app_certificate ------- {}".format(app_certificate))

        if passed_data["is_patient"] is True:
            # Patients token
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_certificate, channel_name, user_account, Role_Subscriber, privilege_expired_ts)
            return Response({'token': token, 'appID': app_id}, status.HTTP_200_OK)
        else:
            passed_data = request.data
            session = CallsOrder.objects.get(session_id=passed_data["channel_name"])
            serializer = CallsOrderSerializer(
                session, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Doctors token
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_certificate, channel_name, user_account, Role_Subscriber, privilege_expired_ts)

            return Response({'token': token, 'appID': app_id}, status.HTTP_200_OK)


class SFToken(views.APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data
        app_id = 'ecfc8ba2d43744588161f36ff1c71cfc'
        app_certificate = '8c5f930076ca44108b93099d06020376'
        channel_name = passed_data["channel_name"]
        user_account = passed_data["callUid"]
        expire_time_in_seconds = 7200
        current_timestamp = int(time.time())
        privilege_expired_ts = current_timestamp + expire_time_in_seconds

        if passed_data["is_patient"] is True:
            # Started by trainer
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_certificate, channel_name, user_account, Role_Subscriber, privilege_expired_ts)

            return Response({'token': token, 'appID': app_id}, status.HTTP_200_OK)
        else:
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_certificate, channel_name, user_account, Role_Publisher, privilege_expired_ts)

            return Response({'token': token, 'appID': app_id, 'isStarted': True}, status.HTTP_200_OK)
