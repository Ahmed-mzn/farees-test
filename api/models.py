from django.db import models
from django.utils import timezone
import binascii
import os
import uuid
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
# image = models.FileField(null=True, blank=True, upload_to='static/images')


class APILog(models.Model):
    request_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_params = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    response_status = models.IntegerField()
    response_body = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.response_status} - {self.path} - {self.user_email} - {self.request_date.day}/{self.request_date.month}/{self.request_date.year} {self.request_date.hour}:{self.request_date.minute}:{self.request_date.second}"
    
    
    
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, last_name, first_name, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(last_name, first_name, password, **other_fields)

    def create_user(self,  last_name, first_name, password, **other_fields):
        
        user = self.model( last_name=last_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    
    ADMIN = 'ADMIN'
    COACH = 'COACH'
    PARENT = 'PARENT'

    ROLE_CHOICES = (
        (ADMIN, 'ADMIN'),
        (COACH, 'COACH'),
        (PARENT, 'PARENT'),
    )
    
    
    email = models.EmailField(_('email address'), unique=True)
    username= models.CharField(max_length=100, unique=False)
    role= models.CharField(max_length=20,null=False, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    telephone = models.IntegerField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    profile_picture = models.FileField(null=True, blank=True, upload_to='static/images')
    doc1 = models.FileField(null=True, blank=True, upload_to='static/documents')
    doc2 = models.FileField(null=True, blank=True, upload_to='static/documents')
    
    
    
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telephone']

    def __str__(self):
        return self.email
        
    class Meta:
        db_table = "USERS"
        # swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=False)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, unique=False)
    telephone = models.IntegerField(null=False, unique=True)
    partner_name = models.CharField(max_length=100, unique=False, default="")
    partner_percentage = models.FloatField(default=0.0)
    def __str__(self):
        return self.name
    
class Branch_image(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branche_image')
    picture = models.ImageField( upload_to='static/images', blank=True, null=True)
    
    def __str__(self):
        return self.branch.name

class PermissionCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name

class PermissionName(models.Model):
    category = models.ForeignKey(PermissionCategory, on_delete=models.CASCADE, related_name='permissions')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True) 

    class Meta:
        unique_together = ('category', 'name') 

    def __str__(self):
        return f"{self.category.name}: {self.name}"


class UserPermissionAssign(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user_permissions_assign')
    permission = models.ForeignKey(PermissionName, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_permissions')

    def __str__(self):
        return f"{self.user.username}: {self.permission}"
    
    
    
class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
class SubscriptionType(models.Model):
    type = models.CharField(max_length=100)
    delai = models.CharField(max_length=20)  # "month", "3 months", or "year"
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type} - {self.delai}"
    
    
    
    
class Class(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    age_from = models.IntegerField()
    age_to = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.age_from} - {self.age_to})"
    
class ClassSubscriptionType(models.Model):
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.class_name} - {self.subscription_type}"
    
    
class Coach(models.Model):
    user = models.OneToOneField('NewUser', on_delete=models.CASCADE)
    doc1 = models.FileField(upload_to='static/coaches/docs', null=True, blank=True)
    doc2 = models.FileField(upload_to='static/coaches/docs', null=True, blank=True)

    def __str__(self):
        return self.user.username


    
class CoachBranch(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.coach} - {self.branch}"
    
    
class Stadium(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50) 
    location = models.URLField(max_length=200)
    photos = models.ImageField(upload_to='static/stadiums/photos', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.branch}"


class WorkingDays(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    day_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.branch} - {self.day_name}"
    
    
class TimingPeriods(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    show_in_app = models.BooleanField(default=True)
    from_time = models.TimeField()
    to_time = models.TimeField()
    days = models.ManyToManyField(WorkingDays)

    def __str__(self):
        return f"{self.name} - {self.branch}"
    
    
class TimingPeriodsLevels(models.Model):
    timing_period = models.ForeignKey(TimingPeriods, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timing_period} - {self.class_name}"
    
    
class Subscriber(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    parent = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Parent: {self.parent.username})"
    
    
class TrainingSessions(models.Model):
    timing_period_level = models.ForeignKey(TimingPeriodsLevels, on_delete=models.CASCADE)

    def __str__(self):
        return f"Session for {self.timing_period_level}"
    
    
    
class SubscriberTraining(models.Model):
    training_session = models.ForeignKey(TrainingSessions, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    child_name = models.CharField(max_length=100)
    parent_entity = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.child_name} - {self.training_session}"
    
    
class OtpMail(models.Model):
    telephone = models.IntegerField(null=False, unique=True)
    otp = models.IntegerField(default=0)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.telephone} {self.otp}"

    class Meta:
        db_table = "OTP_SMS"
        verbose_name = 'Otp sms'
        verbose_name_plural = 'SMSs OTPs'