# Generated by Django 5.1.1 on 2024-09-25 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_rename_text_comment_body_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.CharField(db_index=True, default='Anonymous', max_length=125),
        ),
    ]
