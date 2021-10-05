from django.urls import path
from .views import (DoctorRequest, TokenGenerator,
                    SpecificRequest, GetUserRequests,
                    GetTherapistRequests, TimeSchedule, SFToken,
                    GetDoctorsSchedule, GetDoctorsDateRequests)

urlpatterns = [

    path('',
         DoctorRequest.as_view(),
         name="DoctorRequest"
         ),

    path('<session_id>',
         SpecificRequest.as_view(),
         name="SpecificRequest"
         ),

    path('patient/<patient_id>',
         GetUserRequests.as_view(),
         name="GetUserRequests"
         ),

    path('doc/<doctor_id>',
         GetTherapistRequests.as_view(),
         name="Get Therapist Requests"
         ),

    path('token/',
         TokenGenerator.as_view(),
         name="TokenGenerator"
         ),

    path('tokenify/',
         SFToken.as_view(),
         name="TokenGenerator"
         ),

    path('schedule/',
         TimeSchedule.as_view(),
         name="Doctors Schedule"
         ),

    path('schedule/<doctor_id>',
         GetDoctorsSchedule.as_view(),
         name="Get Doctors Schedule"
         ),

    path('schedule/<scheduled_date>/<doctor_id>',
         GetDoctorsDateRequests.as_view(),
         name="Get the Dates Schedule"
         ),
]
