# Generated by Django 5.0.1 on 2024-01-24 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_posts_post_category_alter_users_email_access_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='post_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.posts'),
        ),
    ]