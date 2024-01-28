# Generated by Django 5.0.1 on 2024-01-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_users_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='post_category',
            field=models.CharField(choices=[('р', 'Ручная живопись'), ('к', 'Компьютерная живопись')], default='р', max_length=1),
        ),
        migrations.AlterField(
            model_name='users',
            name='email_access',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
