# Generated by Django 4.2.1 on 2023-05-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login_Register', '0007_customuser_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default=None, null=True, upload_to='profile_images/'),
        ),
    ]