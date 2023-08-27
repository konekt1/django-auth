from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import UserManager
import uuid


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

class User(AbstractUser, PermissionsMixin):

    USER_ROLE = (
        ('intern', 'Intern'),
        ('recruiter', 'Recruiter'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=12, choices=USER_ROLE,  null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def save_otp(self, otp):
        self.otp = otp
        self.save()


    def compare_otp(self, otp):
        return self.otp == otp

    def __str__(self):
        return self.email

    is_staff = models.BooleanField(
        default=False,  # You can set this to True if you want staff members by default
        help_text='Designates whether the user can log into this admin site.'
    )
    
    is_verified = models.BooleanField(
        default=False,
        help_text='Designates whether the user is verified.'
    )
    
    objects = UserManager()

    # Override is_staff setter if necessary
    def set_staff_status(self, value):
        self.is_staff = value
        self.save()
    
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



class InternProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.IntegerField(default=None, null=True)
    current_location = models.CharField(choices=STATE_CHOICES, max_length=100, default='Abia')
    intern_category = models.CharField(choices=INTERN_CHOICE, max_length=100, default='About to graduate')


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, null=False)
    company_size = models.CharField(choices=SIZE_CHOICE, max_length=100, default="Company Size")
    established_year = models.CharField(choices=ESTABLISHED_CHOICE, max_length=100, default="Established Year")
    company_website = models.CharField(default="Enter Website Name", max_length=100)
    company_url = models.CharField(default="Enter Websiter URL", max_length=100)
    company_mission = models.TextField(default=None, validators=[MaxLengthValidator(500)], null=True)
    about_us = models.CharField(choices=ABOUT_CHOICE, max_length=100, default="Select")