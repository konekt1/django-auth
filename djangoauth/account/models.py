from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractUser


# custom user manager
STATE_CHOICES = (
    ('Abia', 'Abia (Umuahia)'),
    ('Adamawa', 'Adamawa (Yola)'),
    ('Akwa Ibom', 'Akwa Ibom (Uyo)'),
    ('Anambra', 'Anambra (Awka)'),
    ('Bauchi', 'Bauchi (Bauchi)'),
    ('Bayelsa', 'Bayelsa (Yenagoa)'),
    ('Benue', 'Benue (Makurdi)'),
    ('Borno', 'Borno (Maiduguri)'),
    ('Cross River', 'Cross River (Calabar)'),
    ('Delta', 'Delta (Asaba)'),
    ('Ebonyi', 'Ebonyi (Abakaliki)'),
    ('Edo', 'Edo (Benin City)'),
    ('Ekiti', 'Ekiti (Ado Ekiti)'),
    ('Enugu', 'Enugu (Enugu)'),
    ('Gombe', 'Gombe (Gombe)'),
    ('Imo', 'Imo (Owerri)'),
    ('Jigawa', 'Jigawa (Dutse)'),
    ('Kaduna', 'Kaduna (Kaduna)'),
    ('Kano', 'Kano (Kano)'),
    ('Katsina', 'Katsina (Katsina)'),
    ('Kebbi', 'Kebbi (Birnin Kebbi)'),
    ('Kogi', 'Kogi (Lokoja)'),
    ('Kwara', 'Kwara (Ilorin)'),
    ('Lagos', 'Lagos (Ikeja)'),
    ('Nasarawa', 'Nasarawa (Lafia)'),
    ('Niger', 'Niger (Minna)'),
    ('Ogun', 'Ogun (Abeokuta)'),
    ('Ondo', 'Ondo (Akure)'),
    ('Osun', 'Osun (Osogbo)'),
    ('Oyo', 'Oyo (Ibadan)'),
    ('Plateau', 'Plateau (Jos)'),
    ('Rivers', 'Rivers (Port Harcourt)'),
    ('Sokoto', 'Sokoto (Sokoto)'),
    ('Taraba', 'Taraba (Jalingo)'),
    ('Yobe', 'Yobe (Damaturu)'),
    ('Zamfara', 'Zamfara (Gusau)'),
)

INTERN_CHOICE = (
    ('About to graduate', 'About to graduate'),
    ('Just graduated', 'Just graduated'),
    ('Looking to change fields', 'Looking to change fields'),
)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, current_location, intern_category, password=None, confirm_password=None):
        """
        Creates and saves a User with the given email, name
        and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            current_location=current_location,
            intern_category=intern_category,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, current_location, intern_category, password=None):
        """
        Creates and saves a superuser with the given email, name
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            current_location=current_location,
            intern_category=intern_category,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(default=None, null=True)
    current_location = models.CharField(choices=STATE_CHOICES, max_length=100, default='Abia')
    intern_category = models.CharField(choices=INTERN_CHOICE, max_length=100, default='About to graduate')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "current_location", "intern_category"]

    def save_otp(self, otp):
        self.otp = otp
        self.save()

    def compare_otp(self, otp):
        return self.otp == otp

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admin users are staff
        return self.is_admin
    
ABOUT_CHOICE = (
    ('Word of mouth', 'Word of mouth'),
    ('Facebook', 'Facebook'),
    ('Linkedin', 'Linkedin'),
    ('Reddit', 'Reddit'),
    ('AD', 'AD'),
)

ESTABLISHED_CHOICE = (
    ('2023', '2023'),
    ('2022', '2022'),
    ('2021', '2021'),
    ('2020', '2020'),
    ('2019', '2019'),
    ('2018', '2018'),
)

SIZE_CHOICE = (
    ('1-50', '1-50'),
    ('51-100', '51-100'),
    ('100-1000', '100-1000'),
    ('1000-5000', '1000-5000'),
    ('<5000', '<5000'),
    
)


class Recruiter(models.Model):
    company_size = models.CharField(choices=SIZE_CHOICE, max_length=100, default="Company Size")
    established_year = models.CharField(choices=ESTABLISHED_CHOICE, max_length=100, default="Established Year")
    company_website = models.CharField(default="Enter Website Name", max_length=100)
    company_url = models.CharField(default="Enter Websiter URL", max_length=100)
    company_mission = models.TextField(default=None, validators=[MaxLengthValidator(500)])
    about_us = models.CharField(choices=ABOUT_CHOICE, max_length=100, default="Select")


    
