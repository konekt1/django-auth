from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be superuser')
        if extra_fields.get('is_verified') is not True:
            raise ValueError('Superuser must be verified')

        user = self.create_user(email, password, **extra_fields)
        # Set is_admin attribute to True
        user.is_admin = True
        # Set is_staff attribute to True
        user.is_staff = True
        user.save()

        return user
    
    