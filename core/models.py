from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ("receptionist", "Receptionist"),
        ("doctor", "Doctor"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    
from django.db import models


class Patient(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    hospital_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        editable=False
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    national_id = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Save first so Django generates the primary key
        if not self.pk:
            super().save(*args, **kwargs)

        # Generate Hospital ID only once
        if not self.hospital_id:
            self.hospital_id = f"MTRH{self.pk:04d}"
            super().save(update_fields=["hospital_id"])

    def __str__(self):
        return f"{self.hospital_id} - {self.first_name} {self.last_name}"
    
    
class Visit(models.Model):
    STATUS_CHOICES = (
        ("waiting", "Waiting"),
        ("serving", "Being Served"),
        ("completed", "Completed"),
    )

    DEPARTMENT_CHOICES = (
        ("triage", "Triage"),
        ("doctor", "Doctor"),
        ("laboratory", "Laboratory"),
        ("pharmacy", "Pharmacy"),
        ("completed", "Completed"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="visits"
    )

    queue_number = models.CharField(
        max_length=10,
        editable=False,
        blank=True
    )

    current_department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES,
        default="triage"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="waiting"
    )

    

    visit_date = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.queue_number:

            today = timezone.now().date()

            last_visit = Visit.objects.filter(
                visit_date__date=today
            ).order_by("-id").first()

            if last_visit:
                last_number = int(last_visit.queue_number[1:])
                next_number = last_number + 1
            else:
                next_number = 1

            self.queue_number = f"A{next_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.queue_number} - {self.patient}"
    
class Triage(models.Model):
    PRIORITY_CHOICES = (
        ("normal", "Normal"),
        ("urgent", "Urgent"),
        ("emergency", "Emergency"),
    )

    visit = models.OneToOneField(
        Visit,
        on_delete=models.CASCADE,
        related_name="triage"
    )

    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    blood_pressure = models.CharField(
        max_length=20,
        blank=True
    )

    pulse_rate = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    oxygen_saturation = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal"
    )

    notes = models.TextField(
        blank=True
    )
    
    def __str__(self):
        return f"{self.visit.queue_number} - Triage"