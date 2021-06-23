from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone


class UserManager(auth_models.BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email, is_staff=False,
            is_superuser=False, is_active=True,
            date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField('Email address', unique=True)
    first_name = models.CharField(
        'First name', max_length=255, blank=True)
    last_name = models.CharField(
        'Last name', max_length=255, blank=True)
    twitter_id = models.CharField(
        "Twitter ID", max_length=50, unique=True, blank=True)
    is_staff = models.BooleanField(
        'Staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                  'site.')
    is_active = models.BooleanField(
        'Active', default=True,
        help_text='Designates whether this user should be treated as '
                  'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('Date joined',
                                       default=timezone.now)
    key = models.CharField(
        max_length=128, db_index=True, blank=True,
        null=True, unique=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the usmessageer.
        """
        return self.first_name
