from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone

from workwithme import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from core.models import ProfessionalType
from django_countries.fields import CountryField

_USER_PROFESSION = (
    ('S', 'Software developer'),
    ('D', 'Web designer'),
    ('G', 'Graphic Designe'),
)
_MARITAL_STATUS = (
    ('M', 'Married'),
    ('S', 'Single'),
)


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a `User` with an email and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):

        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, ):
    profile_pc = models.ImageField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=16, unique=True, blank=True, null=True)
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(null=True, max_length=20)
    last_name = models.CharField(null=True, max_length=20)
    profession_type = models.ForeignKey(ProfessionalType, on_delete=models.SET_NULL,
                                        db_constraint=False, null=True)
    marital_status = models.CharField(max_length=10, choices=_MARITAL_STATUS, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name


class UserProfile(models.Model):
    """
    Profiles are made through collecting data about your app users, in order to piece together who they are and
    what they like, in the form of a profile. They are the representation of the users and they are the outcome of
    the user profiling process. The elements included in a user profile may include geographical location,
    academic and professional background, membership in groups, interests, preferences, opinions, etc.

    """
    # TODO  our next todo: we need to apply  AI here,
    #  This type of data would be seen as descriptive, however, user profiling is improved by
    #  including statistical data gained from monitoring behavioural app data.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profession = models.CharField(max_length=20, null=True, blank=True, choices=_USER_PROFESSION)
    interests = models.CharField(max_length=20, null=True, blank=True)
    preferences = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User Profile'

    def __str__(self):
        return self.user.username


def user_profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)


post_save.connect(user_profile_receiver, sender=settings.AUTH_USER_MODEL)


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=20, null=True)
    country = CountryField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'User address'

    def __str__(self):
        return self.user.username
