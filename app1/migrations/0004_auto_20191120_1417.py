# Generated by Django 2.2.3 on 2019-11-20 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('od', 'organization_director'), ('oe', 'organization_employee'), ('empy', 'employee')], max_length=2),
        ),
    ]
