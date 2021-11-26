from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from dotenv import load_dotenv
from mailjet_rest import Client

import bugsnag
import os
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from .models import DoctorsProfiles
from .serializers import DoctorProfileSerializer
from ..authentication.models import DoctorsActivation


class Profiles(views.APIView):
    """
        Add Profiles details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def put(request):
        passed_data = request.data
        # Check This later
        try:
            participant = DoctorsProfiles.objects.get(user_id=passed_data["user_id"])
            serializer = DoctorProfileSerializer(participant, data=passed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Profile Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class CodeVerify(views.APIView):
    """Verify User code"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add Profiles to DB """
        passed_data = request.data
        try:
            activate = DoctorsActivation.objects.filter(
                user_email=passed_data["email"],
                activation_code=int(passed_data["activation_code"])
            )
            if activate.count() < 1:
                return Response({
                    "status": "Failed",
                    "code": 0,
                    "message": "Update failed, wrong activation code passed"
                }, status.HTTP_200_OK)
            else:
                return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Code Verification: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class DoctorValidation(views.APIView):
    """Activate or Deactivate doctor"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data
        try:
            doctor = DoctorsProfiles.objects.get(user_id=passed_data["user_id"])
            doctor_serializer = DoctorProfileSerializer(
                doctor, passed_data, partial=True
            )
            doctor_serializer.is_valid()
            doctor_serializer.save()

            doctor_profile = DoctorProfileSerializer(doctor).data

            if passed_data["is_activated"]:
                message_body = "Hello {}, your account has been verified. " \
                               "Thank you for working with us".format(doctor_profile["fullname"])
            else:
                message_body = "Hello {}, your account has been deactivated. " \
                               "Contact support for more information".format(doctor_profile["fullname"])

            DoctorValidation.send_activation_email(
                name=doctor_profile["fullname"],
                email=doctor_profile["email"],
                body=message_body)

            return Response(
                {
                    "status": "success"
                }, status.HTTP_200_OK
            )
        except Exception as e:
            print("-------> {}".format(e))
            bugsnag.notify(
                Exception('Doctor active update: {}'.format(e))
            )
            return Response({
                "error": "{}".format(e),
                "status": "failed",
                "code": 0
            }, status.HTTP_200_OK)

    @staticmethod
    def send_activation_email(name, email, body):
        subject = 'Account Activation Status'
        message = EmailTemplates.activation_email(name, body)
        load_dotenv()
        api_key = os.environ['MJ_API_KEY_PUBLIC']
        api_secret = os.environ['MJ_API_KEY_PRIVATE']
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "helloalfie@epitomesoftware.live",
                        "Name": "Hello Alfie"
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": ""
                        }
                    ],
                    "Subject": subject,
                    "HTMLPart": message
                }
            ]
        }
        result = mailjet.send.create(data=data)
        return result.status_code

class ProfilesAllView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        return DoctorsProfiles.objects.filter().order_by('createdAt')


class ProfileSpecificView(ListAPIView):
    """Get a user specific appointments"""
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        return DoctorsProfiles.objects.filter(
            user_id=self.kwargs['userId']
            ).order_by('createdAt')


class SearchDoctor(views.APIView):
    """Search for doctor using keys"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data
        vector = SearchVector('fullname', 'registered_hospital', 'speciality', 'email')
        query = SearchQuery(passed_data["query"])
        doctor = DoctorsProfiles.objects.annotate(
            rank=SearchRank(vector, query)
        ).filter(
            rank__gte=0.001
        ).order_by('-rank')
        return Response(list(doctor.values()), status.HTTP_200_OK)


class EmailTemplates:

    @staticmethod
    def activation_email(name, body):
        return """
        <!DOCTYPE html>
            <html lang="en">
                <body style="text-align:center;">
                    <br/>
                    <img alt="Image" border="0" src="https://res.cloudinary.com/dolwj4vkq/image/upload/v1621418365/HelloAlfie/ic_launcher.png" title="Image" width="300"/>
                    <br/>
                    <br/>
                    <div style="color:#ff7463;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.2; padding:0;">
                        <div style="font-size: 12px; line-height: 1.2; font-family: 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #ff7463; mso-line-height-alt: 14px;">
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 22px; margin: 0;"><span style="font-size: 18px;"><strong><span style="font-size: 18px;"> Hello {}</span></strong></span></p>
                        </div>
                    </div>
                    <div style="color:#555555;font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;line-height:1.2; padding:10px;">
                        <div style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif; font-size: 12px; line-height: 1.2; color: #555555; mso-line-height-alt: 14px;">
                            <p style="font-size: 17px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0; font-family: Verdana, sans-serif;"> Your path to mental wellness administration starts here.</p>
                            <br/>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0; font-family: Verdana, sans-serif;"> {} </p>
                            <br/>
                            <br/>
                        </div>
                    </div>
                </body>
            </html>
        """.format(name, body)
