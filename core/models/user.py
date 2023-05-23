from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager, BaseUserManager
from django.core.mail import send_mail
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(BaseUserManager) :
    
    def create_user(self, email, password, **args) :
        user = self.model(email = email, **args)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields) :
        print(email, password)
        print(extra_fields)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        user = self.create_user(email, password, **extra_fields)
        return user

class CustomUser(AbstractUser) :
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=20)
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=100)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'password']

    objects = CustomUserManager()




    def email_user(self, subject, message, from_email):
        print(self.email)
        print(self.email)
        send_mail(
            subject,
            message,
            "qasas145@gmail.com",
            ["mohamed.sayed14527@yahoo.com"],
        )

    def __str__(self) -> str:
        return f'{self.email}'
    



class Address(models.Model):
    """
    Address
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(CustomUser, verbose_name=_("User"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Address"
    
    