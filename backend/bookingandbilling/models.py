from django.db import models
from django.core.validators import validate_email, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager

class Gender(models.TextChoices):
    MALE = "M", "Male",
    FEMALE = "F", "Female",
    OTHER = "O", "Other",
    PREFER_NOT_TO_SAY = "X", "Prefer Not To Say",


class AccountType(models.TextChoices):
    ADMIN = "A", "Admin",
    INTERPRETER = "I", "Interpreter",
    CUSTOMER = "C", "Customer",


def hex_color_validator(value):
    regex = r"^#[a-fA-F0-9]{6}$"
    message = "Colour must be a valid hexcode including the #"
    validator = RegexValidator(regex=regex, message=message)
    validator(value)


class Tag(models.Model):
    # required
    name = models.CharField(max_length=30, blank=False, unique=True)

    # not required
    colour = models.CharField(
        max_length=7,
        default="#FFFFFF",
        validators=[hex_color_validator]
    )
    
    def __str__(self):
        return f"{self.name} Object"


class Language(models.Model):
    # required
    language_name = models.CharField(blank=False, unique=True)
    
    def __str__(self):
        return f"{self.language_name}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Create and return a regular user with an email, first name, and last name.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Create and return a superuser with email, first name, last name and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)
    
class User(AbstractUser):
    # required
    email = models.EmailField(
        unique=True,
        blank=False,
        validators=[validate_email]
    )
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    
    # not required
    username = models.CharField(
        max_length=150,
        unique=False,
        blank=True
    ) # "Remove" username (keep incase we need it later)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    alt_phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    notes = models.TextField(blank=True, null=True)

    # Use email for authentication instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Attach the custom user manager
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Admin(User):
    class Meta:
        verbose_name = "Admin"


class Interpreter(User):
    # required
    address = models.TextField()
    postcode = models.CharField(max_length=8)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices
    )
    
    # not required    
    tag = models.ManyToManyField(Tag, related_name="interpreters", blank=True)
    languages = models.ManyToManyField(Language, related_name="interpreters", blank=True)
    
    class Meta:
        verbose_name = "Interpreter" # For django admin interface 


class Customer(User):
    # required
    address = models.TextField()
    postcode = models.CharField(max_length=8)
    organisation = models.CharField()

    # not required
    approver = models.ForeignKey(
        Admin,
        null=True,
        on_delete=models.SET_NULL,
        related_name="approved_customers",
        blank=True
    )
    approved = models.BooleanField(default=False)
    email_validated = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Customer" # For django admin interface 


class Appointment(models.Model):
    # required
    customer = models.ForeignKey(
        Customer,
        null=True,
        on_delete=models.SET_NULL,
        related_name="appointments"
    )
    planned_start_time = models.DateTimeField()
    planned_duration = models.TimeField()
    location = models.CharField() # Should be a Location model?
    language = models.ForeignKey(
        Language,
        null=True,
        on_delete=models.SET_NULL,
        related_name="appointments"
    ) # assuming the other language is english

    # not required
    interpreter = models.ForeignKey(
        Interpreter,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="appointments"
    )
    admin = models.ForeignKey(
        Admin,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="appointments"
    )
    company = models.CharField(blank=True, null=True)
    actual_start_time = models.DateTimeField(blank=True, null=True)
    actual_duration = models.TimeField(blank=True, null=True)
    # Should be an enum (like gender?)
    status = models.CharField(default="Upcoming")
    gender_preference = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=True,
        null=True,
        default=Gender.PREFER_NOT_TO_SAY
    )
    notes = models.CharField(max_length=1027, blank=True, null=True)
    active = models.BooleanField(default=True)
    offered_to = models.ManyToManyField(
        Interpreter,
        related_name="offered_appointments",
        blank=True
    )
    invoice_generated = models.BooleanField(default=False)


def validate_non_zero(value):
    if value == 0:
        raise ValidationError("Value cannot be zero.")


class Translation(models.Model):
    # required
    customer = models.ForeignKey(
        Customer,
        null=True,
        on_delete=models.SET_NULL,
        related_name="translations"
    )
    word_count = models.PositiveIntegerField(
        blank=False,
        validators=[validate_non_zero]
    )
    actual_word_count = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[validate_non_zero]
    )
    document = models.FileField(blank=False, upload_to="translation_documents/")
    language = models.ForeignKey(
        Language,
        null=True,
        on_delete=models.SET_NULL,
        related_name="translations"
    )

    # not required
    company = models.CharField(blank=True, null=True)
    interpreter = models.ForeignKey(
        Interpreter,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="translations"
    )
    admin = models.ForeignKey(
        Admin,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="translations"
    )
    notes = models.CharField(max_length=1027, blank=True, null=True)
    active = models.BooleanField(default=True)
    offered_to = models.ManyToManyField(
        Interpreter,
        related_name="offered_translations",
        blank=True
    )
    invoice_generated = models.BooleanField(default=False)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)