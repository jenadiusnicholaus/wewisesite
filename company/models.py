from django.db import models
from django_countries.fields import CountryField


# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=30, null=True, blank=True)
    country = CountryField(max_length=100, null=True, )
    company_email = models.EmailField(max_length=30, null=True, blank=True)
    password1 = models.CharField(max_length=40, null=True)
    password2 = models.CharField(max_length=20, null=True, editable=False, blank=True)
    agreed_to_terms = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'company'

    def __str__(self):
        return self.company_name
