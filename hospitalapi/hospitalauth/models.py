from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class HospitalUserManager(BaseUserManager):
    def create_user(self, name, email, address, date_of_birth, phone_number, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            address = address,
            date_of_birth = date_of_birth,
            phone_number = phone_number

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class HospitalUser(AbstractBaseUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(verbose_name="email address",max_length=255,
        unique=True,)
    address = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=200)
    phone_number = models.IntegerField(default='+0123')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = HospitalUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
