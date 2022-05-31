# Generated by Django 2.2.16 on 2022-05-30 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220530_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='follower',
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
