# Generated by Django 3.0.8 on 2020-08-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsm', '0020_companycmprecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='companycmprecord',
            name='change',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
