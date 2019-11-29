from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Organization(models.Model):#سازمان
    name = models.CharField(max_length=100)#نام سازمان

    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name_plural = 'سازمان ها'


class Profile(models.Model):  # پروفایل افراد
    STATUS = [
        ('od', 'مدیر سازمان'),  # organization_director
        ('oe', 'کارمند سازمان'),  # organization_employee
        ('em', 'کارمند'),  # employee
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization,verbose_name='سازمان کاربر', null=True, blank=True, on_delete=models.CASCADE)#سازمان کاربر
    status = models.CharField(max_length=2, verbose_name='نقش کاربر', null=True, blank=True, choices=STATUS)  # نقش کاربر

    def __str__(self):
        if self.status:
            return (self.user.username + '/' + self.status)

        else:
            return (self.user.username)

    class Meta:
        verbose_name_plural = 'پروفایل'


class Duty(models.Model):  # وظیفه
    profile = models.ForeignKey(Profile,verbose_name='کاربر',  on_delete=models.CASCADE)
    title = models.CharField(verbose_name='عنوان وظیفه', max_length=200)
    explanation = models.TextField(verbose_name='شرح وظیفه')
    inscription_time = models.DateTimeField(verbose_name='زمان ثبت')
    deadline_time = models.DateTimeField(verbose_name='زمان موعد')

    def __str__(self):
        return (self.title + ' / ' + self.profile.user.username)

    class Meta:
        verbose_name_plural = 'وظیفه'

class RequestEMtoOD(models.Model):# درخواست ارتقا کارمند به مدیر سازمان
    STATUS = [
        ('w', 'در انتظار'),
        ('c', 'تایید شده'),
        ('f', 'رد شده'),
    ]

    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    organization = models.CharField(verbose_name='سازمان درخواست شده', max_length=200)#سازمان درخواست شده
    status = models.CharField(verbose_name='وضعیت درخواست', max_length=2, choices=STATUS)#وضعیت درخواست

    def __str__(self):
        return (self.user.username + ' / ' + self.organization)

    class Meta:
        verbose_name_plural = 'درخواست ارتقا کارمند به مدیر سازمان'



class RequestEMtoOE(models.Model):# درخواست ارتقا کارمند به کارمند سازمان
    STATUS = [
        ('w', 'در انتظار'),
        ('c', 'تایید شده'),
        ('f', 'رد شده'),
    ]

    user = models.ForeignKey(User,verbose_name='کاربر',  on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization,verbose_name='سازمان درخواست شده',  on_delete=models.CASCADE)
    status = models.CharField(max_length=2, verbose_name='وضعیت درخواست',  choices=STATUS)

    def __str__(self):
        return (self.user.username + ' / ' + self.organization.name)

    class Meta:
        verbose_name_plural = 'درخواست ارتقا کارمند به کارمند سازمان'


class RequestOEtoOD(models.Model):# درخواست ارتقا کارمند سازمان به مدیر سازمان
    STATUS = [
        ('w', 'در انتظار'),
        ('c', 'تایید شده'),
        ('f', 'رد شده'),
    ]

    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, verbose_name='وضعیت درخواست', choices=STATUS)

    def __str__(self):
        return (self.user.username + '/' + self.user.profile.organization.name)

    class Meta:
        verbose_name_plural = 'درخواست ارتقا کارمند سازمان به مدیر سازمان'
