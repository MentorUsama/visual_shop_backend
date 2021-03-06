# Generated by Django 3.2.9 on 2022-01-22 09:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('contact', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator('^[0-9]{11}$', 'Contact number should consist of 11 digits')])),
                ('jazzCashNumber', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator('^[0-9]{11}$', 'Contact number should consist of 11 digits')])),
                ('cardNumber', models.CharField(blank=True, max_length=30)),
                ('cardExpiryDate', models.DateField(blank=True, null=True)),
                ('CVC', models.IntegerField(blank=True, null=True)),
                ('authType', models.CharField(choices=[('email', 'EMAIL'), ('google', 'GOOGLE')], default='email', max_length=20)),
                ('cityId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.city')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='provinceId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='customer.province'),
        ),
    ]
