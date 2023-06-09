# Generated by Django 4.2.1 on 2023-05-24 10:25

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login_Register', '0006_uploadedfiles_is_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1900, 1, 1), 'Please enter a valid date of birth.'), django.core.validators.MaxValueValidator(datetime.date(2023, 5, 24), 'Please enter a valid date of birth')]),
        ),
    ]
