# Generated by Django 2.2.3 on 2019-11-26 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_auto_20191126_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duty',
            name='duty_explanation',
        ),
        migrations.AddField(
            model_name='duty',
            name='explanation',
            field=models.TextField(default=1, verbose_name='شرح وظیفه'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='duty',
            name='deadline_time',
            field=models.DateTimeField(verbose_name='زمان موعد'),
        ),
        migrations.AlterField(
            model_name='duty',
            name='inscription_time',
            field=models.DateTimeField(verbose_name='زمان ثبت'),
        ),
        migrations.AlterField(
            model_name='duty',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Profile', verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='duty',
            name='title',
            field=models.CharField(max_length=200, verbose_name='عنوان وظیفه'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.Organization', verbose_name='سازمان کاربر'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('od', 'مدیر سازمان'), ('oe', 'کارمند سازمان'), ('em', 'کارمند')], max_length=2, null=True, verbose_name='نقش کاربر'),
        ),
        migrations.AlterField(
            model_name='requestemtood',
            name='organization',
            field=models.CharField(max_length=200, verbose_name='سازمان درخواست شده'),
        ),
        migrations.AlterField(
            model_name='requestemtood',
            name='status',
            field=models.CharField(choices=[('w', 'در انتظار'), ('c', 'تایید شده'), ('f', 'رد شده')], max_length=2, verbose_name='وضعیت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestemtood',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='requestemtooe',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Organization', verbose_name='سازمان درخواست شده'),
        ),
        migrations.AlterField(
            model_name='requestemtooe',
            name='status',
            field=models.CharField(choices=[('w', 'در انتظار'), ('c', 'تایید شده'), ('f', 'رد شده')], max_length=2, verbose_name='وضعیت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestemtooe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='requestoetood',
            name='status',
            field=models.CharField(choices=[('w', 'در انتظار'), ('c', 'تایید شده'), ('f', 'رد شده')], max_length=2, verbose_name='وضعیت درخواست'),
        ),
        migrations.AlterField(
            model_name='requestoetood',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
