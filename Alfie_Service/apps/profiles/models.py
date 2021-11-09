from django.db import models
from datetime import datetime


class DoctorsProfiles(models.Model):
    # Authentication details
    fullname = models.CharField(max_length=250, default='non')
    email = models.CharField(unique=True, max_length=250, default='non')
    activation_code = models.CharField(max_length=250, default='non')
    is_active = models.BooleanField(default=True)  # recently accessed the app, false if took more than a month
    user_id = models.CharField(max_length=350, default='non', unique=True)
    is_activated = models.BooleanField(default=False)
    activated_by = models.CharField(default="", max_length=350)  # Admin id
    # Requests
    fcm = models.TextField(null=True)

    # Personal details
    gender = models.CharField(max_length=250, null=True)
    birthDate = models.DateTimeField(default=datetime.now)
    phone_number = models.CharField(max_length=250, null=True)
    profile_image = models.TextField(
        default="https://res.cloudinary.com/dolwj4vkq/image/upload/v1621418365/HelloAlfie/ic_launcher.png"
    )
    about = models.TextField(null=True)

    # Specialization
    speciality = models.CharField(max_length=250, null=True)
    practice_duration = models.IntegerField(verbose_name='in months', default=0)
    registered_hospital = models.TextField(null=True)
    registration_code = models.CharField(max_length=50,  null=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'email : {} ,fullname: {}'.format(
            self.email, self.fullname)


class PatientProfile(models.Model):
    # Authentication details
    fullname = models.CharField(max_length=250, default='non')
    email = models.CharField(unique=True, max_length=250, default='non')
    activation_code = models.CharField(max_length=250, default='non')
    user_id = models.CharField(max_length=350, default='non', unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Personal details
    gender = models.CharField(max_length=250, null=True)
    birthDate = models.DateTimeField(default=datetime.now)
    location_address = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=250, null=True)
    nationality = models.CharField(max_length=250, null=True)
    profile_image = models.CharField(
        max_length=1250,
        default="https://res.cloudinary.com/dolwj4vkq/image/upload/v1621418365/HelloAlfie/ic_launcher.png"
    )
    fcm = models.CharField(max_length=1050, null=True)
    about = models.TextField(null=True)
    employment = models.CharField(max_length=250, null=True)
    current_employer = models.CharField(max_length=250, null=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'email : {} ,fullname: {}'.format(
            self.email, self.fullname)
