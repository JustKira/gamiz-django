# Generated by Django 4.0.3 on 2022-04-02 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customUser', '0002_customuser_conuntry_customuser_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='firstname',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='lastname',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
