# Generated by Django 3.2.9 on 2022-01-27 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_feedback_customerid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='colourSelected',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='sizeSelected',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]