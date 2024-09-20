# Generated by Django 5.1 on 2024-09-20 21:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'faculties',
            },
        ),
        migrations.CreateModel(
            name='FacultyCoordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coordinator_faculties', to=settings.AUTH_USER_MODEL)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_coordinators', to='faculties.faculty')),
            ],
            options={
                'db_table': 'faculty_coordinators',
            },
        ),
        migrations.CreateModel(
            name='FacultyStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_students', to='faculties.faculty')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_faculties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'faculty_students',
            },
        ),
        migrations.AddField(
            model_name='faculty',
            name='students',
            field=models.ManyToManyField(related_name='faculties', through='faculties.FacultyStudent', to=settings.AUTH_USER_MODEL),
        ),
    ]
