from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Organization(models.Model):  #
    name = models.CharField(max_length=100)

    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name_plural = 'سازمان ها'


class Profile(models.Model):  # پروفایل افراد
    STATUS = [
        ('od', 'organization_director'),  # مدیر سازمان
        ('oe', 'organization_employee'),  # کارمند سازمان
        ('em', 'employee'),  # کارمند
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, null=True, blank=True, choices=STATUS)  # وضعیت کاربر

    def __str__(self):
        if self.status:
            return (self.user.username + '/' + self.status)

        else:
            return (self.user.username)

    class Meta:
        verbose_name_plural = 'پروفایل'


class Duty(models.Model):  # وظیفه
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # عنوان
    duty_explanation = models.TextField()  # شرح وظیفه
    inscription_time = models.DateTimeField()  # زمان ثبت
    deadline_time = models.DateTimeField()  # زمان موعد

    def __str__(self):
        return (self.title + ' / ' + self.profile.user.username)

    class Meta:
        verbose_name_plural = 'وظیفه'

class RequestEMtoOD(models.Model):
    STATUS = [
        ('w', 'waiting'),  # در انتظار
        ('c', 'confirmed'),  # تایید شده
        ('f', 'failed'),  # رده شده
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200)
    status = models.CharField(max_length=2, choices=STATUS)

    def __str__(self):
        return (self.user.username + ' / ' + self.organization)

    class Meta:
        verbose_name_plural = 'درخواست ارتقا کارمند به مدیر سازمان'



class RequestEMtoOE(models.Model):
    STATUS = [
        ('w', 'waiting'),  # در انتظار
        ('c', 'confirmed'),  # تایید شده
        ('f', 'failed'),  # رده شده
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS)

    def __str__(self):
        return (self.user.username + ' / ' + self.organization.name)

    class Meta:
        verbose_name_plural = 'درخواست ارتقا کارمند به کارمند سازمان'


class RequestOEtoOD(models.Model):
    STATUS = [
        ('w', 'waiting'),  # در انتظار
        ('c', 'confirmed'),  # تایید شده
        ('f', 'failed'),  # رده شده
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS)

    def __str__(self):
        return (self.user.username + '/' + self.user.profile.organization.name)

    class Meta:
        verbose_name_plural = 'درخواست ارتقا کارمند سازمان به مدیر سازمان'
