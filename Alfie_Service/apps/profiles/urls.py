from django.urls import path
from .doctors_views import (
     Profiles as DocProfiles,  ProfilesAllView as DocProfilesAllView,
     ProfileSpecificView as DocProfileSpecificView, CodeVerify,
     SearchDoctor, SpecialityView, SpecialitySearch, DoctorValidation
     )
from .patients_views import (
     Profiles,  ProfilesAllView, ProfileSpecificView,
     )

urlpatterns = [

    path('code/',
         CodeVerify.as_view(),
         name="profiles"
         ),

    # doctors
    path('doc/',
         DocProfiles.as_view(),
         name="profiles"
         ),

    path('doc/<userId>',
         DocProfileSpecificView.as_view(),
         name="specific profiles"
         ),

    path('doc/all/',
         DocProfilesAllView.as_view(),
         name="all profiles"
         ),

    path('doc/search/',
         SearchDoctor.as_view(),
         name="Search Doctor"
         ),

    path('doc/speciality/',
         SpecialityView.as_view(),
         name="Doctor SpecialityView"
         ),

    path('doc/speciality/search/',
         SpecialitySearch.as_view(),
         name="Doctor Speciality Search"
         ),

    path('doc/activation/',
         DoctorValidation.as_view(),
         name="Doctor Validation"
         ),

    # Patients
    path('',
         Profiles.as_view(),
         name="profiles"
         ),

    path('<userId>',
         ProfileSpecificView.as_view(),
         name="specific profiles"
         ),

    path('all/',
         ProfilesAllView.as_view(),
         name="all profiles"
         ),
]
