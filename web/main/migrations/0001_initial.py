# Generated by Django 5.0.1 on 2024-01-22 18:00

import django.core.validators
import django.db.models.deletion
import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('login', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=8)),
                ('email', models.EmailField(max_length=254)),
                ('email_access', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('post_title', models.CharField(max_length=16)),
                ('post_image', models.ImageField(upload_to='')),
                ('post_date', models.DateTimeField(default=main.models.getTimeNow, editable=False)),
                ('img_price', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0, message='Цена не может быть ниже 0')])),
                ('post_likes', models.IntegerField(default=0, editable=False)),
                ('author_login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_content', models.TextField()),
                ('comment_date', models.DateTimeField(default=main.models.getTimeNow, editable=False)),
                ('author_login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
            ],
        ),
        migrations.CreateModel(
            name='UsersRights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('right_date', models.DateTimeField(default=main.models.getTimeNow, editable=False)),
                ('author_login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.posts')),
            ],
        ),
    ]
