# Generated by Django 5.1 on 2024-10-16 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='student_organizer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_organizer', to='user.student'),
        ),
    ]
