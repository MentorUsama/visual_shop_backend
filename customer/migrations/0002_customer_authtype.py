# Generated by Django 3.2.9 on 2021-12-13 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='authType',
            field=models.CharField(choices=[('email', 'EMAIL'), ('google', 'GOOGLE')], default='email', max_length=20),
        ),
    ]