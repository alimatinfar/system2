# Generated by Django 2.2.3 on 2019-11-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_auto_20191124_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='duty',
            options={'verbose_name_plural': 'وظیفه'},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name_plural': 'سازمان ها'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'پروفایل'},
        ),
        migrations.AlterModelOptions(
            name='requestemtood',
            options={'verbose_name_plural': 'درخواست ارتقا کارمند به مدیر سازمان'},
        ),
        migrations.AlterModelOptions(
            name='requestemtooe',
            options={'verbose_name_plural': 'درخواست ارتقا کارمند به کارمند سازمان'},
        ),
        migrations.AlterModelOptions(
            name='requestoetood',
            options={'verbose_name_plural': 'درخواست ارتقا کارمند سازمان به مدیر سازمان'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('od', 'مدیر سازمان'), ('oe', 'کارمند سازمان'), ('em', 'کارمند')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='requestemtood',
            name='status',
            field=models.CharField(choices=[('w', 'در انتظار'), ('c', 'تایید شده'), ('f', 'رد شده')], max_length=2),
        ),
        migrations.AlterField(
            model_name='requestemtooe',
            name='status',
            field=models.CharField(choices=[('w', 'در انتظار'), ('c', 'تایید شده'), ('f', 'رد شده')], max_length=2),
        ),
        migrations.AlterField(
            model_name='requestoetood',
            name='status',
            field=models.CharField(choices=[('w', 'در انتظار'), ('c', 'تایید شده'), ('f', 'رد شده')], max_length=2),
        ),
    ]
