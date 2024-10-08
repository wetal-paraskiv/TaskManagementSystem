# Generated by Django 5.1.1 on 2024-09-27 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_text', models.CharField(db_index=True, max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=125)),
                ('description', models.CharField(db_index=True, max_length=255)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
