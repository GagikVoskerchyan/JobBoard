# Generated by Django 4.2.7 on 2025-05-05 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_date_applied_application_applied_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]
