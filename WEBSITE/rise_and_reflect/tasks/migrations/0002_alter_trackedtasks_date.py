# Generated by Django 3.2.20 on 2024-06-18 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackedtasks',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
