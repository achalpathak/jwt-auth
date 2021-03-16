# Generated by Django 3.1.7 on 2021-03-14 12:00

from django.db import migrations, models
import jwtAuthentication.userAuth.utils


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to=jwtAuthentication.userAuth.utils.user_profile_photo_path),
        ),
    ]