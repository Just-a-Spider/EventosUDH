# Generated by Django 5.1 on 2024-09-20 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Estudiante'), ('coordinator', 'Coordinador'), ('speaker', 'Ponente')], default='student', max_length=20),
        ),
    ]