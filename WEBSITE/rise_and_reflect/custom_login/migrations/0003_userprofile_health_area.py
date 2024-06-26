# Generated by Django 3.2.20 on 2023-08-03 23:46

from django.db import migrations
from daily_commitments.models import HEALTH_AREAS


def create_health_areas(apps, schema_editor):
    UserHealthArea = apps.get_model('daily_commitments', 'UserHealthArea')
    Tasks = apps.get_model('tasks', 'Tasks')

    user_health_area1 = UserHealthArea(health_area=HEALTH_AREAS[0][0])
    user_health_area1.save()
    area_1_task_list = ["Practice mindfulness meditation", "Prepare and savor a calming herbal tea", "Light stretching or yoga session", "Listen to a guided relaxation or calming music", "Take a walk in nature", "Doing deep breathing exercises", "List of achievable tasks to reduce overwhelm", "List things I'm grateful for", "Light Exercise"]
    for task1 in area_1_task_list:

        suggested_task_for_1_eve = Tasks(health_area=user_health_area1, task=task1, task_type="Evening")
        suggested_task_for_1_eve.save()
        suggested_task_for_1_morn = Tasks(health_area=user_health_area1, task=task1, task_type="Morning")
        suggested_task_for_1_morn.save()
    
    user_health_area2 = UserHealthArea(health_area=HEALTH_AREAS[1][0])
    user_health_area2.save()
    area_2_task_list = ["Meditate on your emotions", "Write in a journal to explore your feelings and goals", "Read a personal development book or inspirational quotes", "Practice affirmations to build self-confidence and positivity", "Review your long-term goals", "Reflect on the positive aspects of your life and accomplishments", "Listen to a motivational podcast or TED talk"]
    for task2 in area_2_task_list:

        suggested_task_for_2_eve = Tasks(health_area=user_health_area2, task=task2, task_type="Evening")
        suggested_task_for_2_eve.save()
        suggested_task_for_2_morn = Tasks(health_area=user_health_area2, task=task2, task_type="Morning")
        suggested_task_for_2_morn.save()
    
    user_health_area3 = UserHealthArea(health_area=HEALTH_AREAS[2][0])
    user_health_area3.save()
    area_3_task_list = ["Start your day with a glass of lemon water", "Engage in a 20-minute workout or physical activity", "Prepare a nutritious breakfast", "Spend time outdoors", "Reach out to family members or friends","Tim for personal grooming and/or self-care"]

    for task3 in area_3_task_list:
        suggested_task_for_3_eve = Tasks(health_area=user_health_area3, task=task3, task_type="Evening")
        suggested_task_for_3_eve.save()
        suggested_task_for_3_morn = Tasks(health_area=user_health_area3, task=task3, task_type="Morning")
        suggested_task_for_3_morn.save()

    user_health_area4 = UserHealthArea(health_area=HEALTH_AREAS[3][0])
    user_health_area4.save()
    area_4_task_list = ["Practice mindfulness meditation", "Exercise to release tension", "Write a gratitude list for positivity", "Journal feelings, gain perspective", "Positive affirmations for self-compassion", "Try a creative outlet"]

    for task4 in area_4_task_list:
        suggested_task_for_4_eve = Tasks(health_area=user_health_area4, task=task4, task_type="Evening")
        suggested_task_for_4_eve.save()
        suggested_task_for_4_morn = Tasks(health_area=user_health_area4, task=task4, task_type="Morning")
        suggested_task_for_4_morn.save()

    user_health_area = UserHealthArea(health_area=HEALTH_AREAS[4][0])
    user_health_area.save()
    suggested_task_for_eve = Tasks(health_area=user_health_area, task="Eve task for " + HEALTH_AREAS[4][0], task_type="Evening")
    suggested_task_for_eve.save()
    suggested_task_for_morn = Tasks(health_area=user_health_area, task="Morn task for " + HEALTH_AREAS[4][0], task_type="Morning")
    suggested_task_for_morn.save()

class Migration(migrations.Migration):

    dependencies = [
        ('daily_commitments', '0001_initial'),
        ('tasks', '0001_initial'),
        ('custom_login', '0002_userprofile_health_area'),
    ]

    operations = [
        migrations.RunPython(create_health_areas),
    ]