# Generated by Django 4.0.3 on 2022-09-12 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customUser', '0009_customuser_is_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='district',
            new_name='building',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='governorate',
            new_name='city',
        ),
        migrations.AddField(
            model_name='customuser',
            name='street_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]