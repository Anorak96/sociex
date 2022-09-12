# Generated by Django 3.2 on 2022-08-09 22:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=40, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True, verbose_name='username')),
                ('cover_pic', models.ImageField(blank=True, default=user.models.get_default_cover_image, null=True, upload_to=user.models.get_cover_image, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('profile_pic', models.ImageField(blank=True, default=user.models.get_default_profile_image, null=True, upload_to=user.models.get_profile_image, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('date_joined', models.DateField(verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('hide_email', models.BooleanField(default=True)),
                ('follower', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='followings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]