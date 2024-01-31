from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class BaseUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_customer = False
        user.is_seller = True

        user.save(using=self._db)

        return user




class Account(AbstractUser):
    username = models.CharField(max_length=75, unique=True)
    first_name = models.CharField(max_length=75)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    last_name = models.CharField(max_length=75)
    phone_number = models.CharField(max_length=15, blank=True)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = BaseUserManager()


    def __str__(self):
        return self.email
    

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def has_perm(self, perm, obj=None):
        return self.is_admin


    def has_module_perms(self, app_label):
        return True



class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="userprofile/", blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=75, blank=True)
    state = models.CharField(max_length=75, blank=True)
    country = models.CharField(max_length=75, blank=True)


    def __str__(self):
        return self.user.first_name

    
    def full_address(self):
        return f"{self.address_line1}, {self.city}, {self.country}"