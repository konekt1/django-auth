from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

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

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
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

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "current_location", "intern_category"]

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
