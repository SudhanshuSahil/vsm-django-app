# Generated by Django 3.0.8 on 2020-08-16 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsm', '0015_auto_20200816_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vsmprofile',
            name='cash',
            field=models.DecimalField(decimal_places=10, default=1000000, max_digits=50),
        ),
        migrations.AlterField(
            model_name='vsmprofile',
            name='is_iitb',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
