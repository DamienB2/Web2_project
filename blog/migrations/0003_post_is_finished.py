# Generated by Django 4.2.7 on 2023-12-06 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_post_content_post_access_code_post_alignment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
