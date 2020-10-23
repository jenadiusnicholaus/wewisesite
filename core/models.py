from django.db import models
from django.utils import timezone

from workwithme import settings


class ProfessionalType(models.Model):
    type = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'professional type'

    def __str__(self):
        return self.type


class JobType(models.Model):
    type = models.CharField(max_length=30, null=True)
    created_on = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        verbose_name_plural = 'Job type'

    def __str__(self):
        return self.type


class Jobs(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return self.job_title


class Suggestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "Suggestion"

    def __str__(self):
        return self.job
