# Generated by Django 5.1 on 2024-10-16 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('faculties', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='coordinator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='user.coordinator'),
        ),
        migrations.AddField(
            model_name='facultystudent',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_students', to='faculties.faculty'),
        ),
        migrations.AddField(
            model_name='facultystudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_faculties', to='user.student'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='students',
            field=models.ManyToManyField(related_name='faculties', through='faculties.FacultyStudent', to='user.student'),
        ),
        migrations.AlterUniqueTogether(
            name='facultystudent',
            unique_together={('faculty', 'student')},
        ),
    ]
