# Generated by Django 3.2.20 on 2024-06-21 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('track_routine', '0001_initial'),
        ('tasks', '0002_alter_trackedtasks_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackedtasks',
            name='personal_routine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_routine', to='track_routine.routinetasks', verbose_name='personal_routine'),
        ),
    ]
