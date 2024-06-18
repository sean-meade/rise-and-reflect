from django.db.models import Max
from .models import PersonalTasks


def get_max_order(user) -> int:
    existing_ptasks = PersonalTasks.objects.filter(user=user)
    if not existing_ptasks.exists():
        return 1
    else:
        current_max = existing_ptasks.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1

def reorder(user):
    existing_ptasks = PersonalTasks.objects.filter(user=user)
    if not existing_ptasks.exists():
        return
    number_of_films = existing_ptasks.count()
    new_ordering = range(1, number_of_films+1)
    
    for order, user_film in zip(new_ordering, existing_ptasks):
        user_film.order = order
        user_film.save()

def rename_keys(list_of_dicts):
    new_list_of_dicts = []
    for current_dict in list_of_dicts:
        new_dict = {}
        for key, value in current_dict.items():
            # Split the key by '__' and take the last part
            new_key = key.split('__')[-1]
            new_dict[new_key] = value
        new_list_of_dicts.append(new_dict)
    return new_list_of_dicts