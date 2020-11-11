from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from authentication.models import UserSkills

from workwithme import settings


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
    skills_needed = models.ManyToManyField(UserSkills)
    job_title = models.CharField(max_length=100, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    publish_end_date = models.DateTimeField(auto_created=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return self.job_title


class CompanyOverview(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
