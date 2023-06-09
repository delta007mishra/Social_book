# Generated by Django 4.2.1 on 2023-05-22 04:27

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login_Register', '0004_uploadedfiles_user_alter_customuser_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1900, 1, 1), 'Please enter a valid date of birth.'), django.core.validators.MaxValueValidator(datetime.date(2023, 5, 22), 'Please enter a valid date of birth.')]),
        ),
    ]
