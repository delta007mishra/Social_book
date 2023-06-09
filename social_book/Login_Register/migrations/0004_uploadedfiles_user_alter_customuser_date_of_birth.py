# Generated by Django 4.2.1 on 2023-05-20 11:17

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login_Register', '0003_alter_customuser_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfiles',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1900, 1, 1), 'Please enter a valid date of birth.'), django.core.validators.MaxValueValidator(datetime.date(2023, 5, 20), 'Please enter a valid date of birth.')]),
        ),
    ]
