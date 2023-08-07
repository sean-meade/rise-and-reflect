# Generated by Django 3.2.20 on 2023-08-07 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutineTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(auto_now=True, verbose_name='routine_day')),
                ('routine_type', models.CharField(choices=[('Evening', 'Evening'), ('Morning', 'Morning')], max_length=9)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_routine_fid', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
