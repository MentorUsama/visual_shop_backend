# Generated by Django 3.2.9 on 2022-02-13 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20220127_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='strip_client_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]