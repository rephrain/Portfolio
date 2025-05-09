# Generated by Django 5.1.6 on 2025-04-21 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('porto', '0005_remove_project_skill_project_skill'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='resumes/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_at']},
        ),
    ]
