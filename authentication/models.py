from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django_countries.fields import CountryField
from workwithme import settings
from PIL import Image

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
        user.is_active = False
        user.is_staff = False
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
    profile_pc = models.ImageField(upload_to='ProfilePics', max_length=100, null=True, blank=True,
                                   default='media/default.png')
    username = models.CharField(max_length=16, unique=True, blank=True, null=True)
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(null=True, max_length=20)
    last_name = models.CharField(null=True, max_length=20)
    profession = models.CharField(max_length=39, null=True)
    marital_status = models.CharField(max_length=10, choices=_MARITAL_STATUS, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password2 = models.CharField(max_length=40, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True)
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

        return str(self.username)

    def get_short_name(self):
        return str(self.username)

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
    interests = models.CharField(max_length=20, null=True, blank=True)
    preferences = models.CharField(max_length=30, null=True, blank=True)
    experiences = models.IntegerField(default=0)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super().save()
    #
    #     img = Image.open(self.profile_pc.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pc.path)

    class Meta:
        verbose_name_plural = 'User Profile'

    def __str__(self):
        return str(self.user.username)

    @property
    def get_full_name(self):
        return f'{str(self.user.first_name)} {str(self.user.last_name)}'

    @property
    def get_follower(self):
        """ """
        return Follow.objects.filter(follower=self.user).count()

    def get_following(self):
        return Follow.objects.filter(user_id=self.user).count()


def user_profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)


class Follow(models.Model):
    user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, null=True)
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        verbose_name_plural = 'Follow and following'
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'follower'], name="unique_followers")
        ]

        ordering = ["-created_on"]

    def __str__(self):
        return f'{self.user_id} follows {self.follower}'

    @property
    def Notify_following(self):
        return f'{self.user_id} follows {self.follower}'


post_save.connect(user_profile_receiver, sender=settings.AUTH_USER_MODEL)


class UserOverview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "User description"

    def __str__(self):
        return str(self.user)


class UserProfessionalType(models.Model):
    type = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User professional type'

    def __str__(self):
        return self.type


class UserSkills(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    skill_title = models.CharField(max_length=200, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'User Skills'


class UserExperiences(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    experience_title = models.CharField(max_length=200, null=True)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'User Experience'

    def __str__(self):
        return self.experience_title


class UserEducation(models.Model):
    programme = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year_from = models.CharField(max_length=30, null=True)
    year_to = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_o = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'User Education'

    def __str__(self):
        return str(self.user)


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=20, null=True)
    country = CountryField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'User address'

    def __str__(self):
        return str(self.user.username)


class UserSuggestions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "User Suggestions"

    def __str__(self):
        return self.job


class UserPortfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    portfolio_link = models.URLField(unique=True, null=True, blank=True)
    web_link = models.URLField(unique=True, null=True, blank=True)
    cover_picture = models.ImageField(upload_to='portfolio_images')
    created_at = models.DateTimeField(default=timezone.now)
    updated_o = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'User portfolio'

    def __str__(self):
        return str(self.user.username)
