# Generated by Django 3.0.8 on 2020-08-12 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsm', '0010_auto_20200812_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='vsmprofile',
            name='college',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]