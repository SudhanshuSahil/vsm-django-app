# Generated by Django 3.0.8 on 2020-08-11 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vsm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VSMProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin_link', models.TextField(blank=True, max_length=500, null=True)),
                ('college', models.TextField(blank=True, max_length=250, null=True)),
                ('city', models.TextField(blank=True, max_length=50, null=True)),
                ('country', models.TextField(blank=True, max_length=50, null=True)),
                ('zip_code', models.TextField(blank=True, max_length=50, null=True)),
                ('about_person', models.TextField(blank=True, max_length=500, null=True)),
                ('token', models.TextField(blank=True, max_length=150, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='VSM_Profile',
        ),
    ]
