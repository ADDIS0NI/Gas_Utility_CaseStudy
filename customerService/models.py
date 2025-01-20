from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class ServiceRequest(models.Model):
    TYPE_CHOICES = [
        ('repair', 'Repair'),
        ('installation', 'Installation'),
        ('maintenance', 'Maintenance'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('assigned', 'Assigned to Team'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_notes = models.TextField(blank=True, help_text="Notes about status changes")
    assigned_team = models.CharField(max_length=100, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.request_type} - {self.status}"

    def update_status(self, new_status, notes=None, team=None, scheduled_date=None):
        self.status = new_status
        if notes:
            self.status_notes = f"{timezone.now().strftime('%Y-%m-%d %H:%M')} - {notes}\n{self.status_notes}"
        if team:
            self.assigned_team = team
        if scheduled_date:
            self.scheduled_date = scheduled_date
        self.save()

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customerservice_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customerservice_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class ServiceFeedback(models.Model):
    RATING_CHOICES = [(i, f"{'★' * i}") for i in range(1, 6)]
    
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Request #{self.service_request.id} - {self.rating} stars"
