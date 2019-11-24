# Generated by Django 2.2.3 on 2019-11-21 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0007_requestoe'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RequestOD',
            new_name='RequestEMtoOD',
        ),
        migrations.RenameModel(
            old_name='RequestOE',
            new_name='RequestEMtoOE',
        ),
        migrations.CreateModel(
            name='RequestOEtoOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]