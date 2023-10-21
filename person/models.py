from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext as _

from team.models import Team


class PersonManager(BaseUserManager):
    """Define a model manager for Person(User) model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a Person(User) with the given email and password."""
        if not email:
            raise ValueError("Email is required field")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular Person(User)
        with the given email and password.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser(Person) with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Person(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    team = models.ForeignKey(
        to=Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="people"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = PersonManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}, id: {self.id}"
