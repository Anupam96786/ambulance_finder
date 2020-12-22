# Generated by Django 3.1.4 on 2020-12-21 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token', models.UUIDField(primary_key=True, serialize=False)),
                ('purpose', models.CharField(choices=[('user_activation', 'User Activation'), ('password_reset', 'Password Reset')], max_length=30, verbose_name='Purpose')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]