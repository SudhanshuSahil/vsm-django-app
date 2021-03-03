# Generated by Django 3.0.8 on 2020-08-16 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vsm', '0019_holding_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCMPRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmp', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vsm.Company')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]