# Generated by Django 2.2.3 on 2019-11-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_auto_20191123_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('od', 'organization_director'), ('oe', 'organization_employee'), ('em', 'employee')], max_length=2, null=True),
        ),
    ]