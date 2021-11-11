from django.db import models


# Create your models here.
class CallsOrder(models.Model):
    session_id = models.CharField(unique=True, max_length=350, default='')
    doctor_id = models.CharField(max_length=350, default='')
    patient_id = models.CharField(max_length=350, default='')
    description = models.CharField(max_length=5050, default='')
    remarks = models.TextField(default='')
    entry_point = models.CharField(max_length=5050, default='')  # Blogs or podcast
    entry_id = models.CharField(max_length=350, default='')  # Based on the above entry
    status = models.CharField(max_length=350, default='PENDING')  # PENDING, CONFIRMED, STARTED, COMPLETED
    scheduled_date = models.CharField(max_length=350, default='')  # for therapists
    scheduled_time = models.CharField(max_length=350, default='')  # for therapists
    scheduled_slot = models.CharField(max_length=350, default='')  # for therapists
    rating = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)  # will show completed date

    def __str__(self):
        """ String representation of db object """
        return 'doctor_id : {} ,description: {}'.format(
            self.doctor_id, self.description)


class DoctorsSchedule(models.Model):
    """Mpdels for doctors weekly schedule"""
    doctor_id = models.CharField(max_length=250, default='non')
    monday = models.CharField(max_length=1250, null=True)
    tuesday = models.CharField(max_length=1250, null=True)
    wednesday = models.CharField(max_length=1250, null=True)
    thursday = models.CharField(max_length=1250, null=True)
    friday = models.CharField(max_length=1250, null=True)
    saturday = models.CharField(max_length=1250, null=True)
    sunday = models.CharField(max_length=1250, null=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)  # will show completed date

    def __str__(self):
        """ String representation of db object """
        return 'doctor_id : {}'.format(self.doctor_id)
