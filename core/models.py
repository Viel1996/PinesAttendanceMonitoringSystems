from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    rfid = models.CharField(max_length=50, unique=True)  # make sure this exists

    def __str__(self):
        return self.name

class ScanLog(models.Model):
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL)
    rfid_code = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)