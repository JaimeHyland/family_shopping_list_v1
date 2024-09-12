from django.contrib.auth.models import Group

def is_adult(user):
    return user.groups.filter(name='adult').exists()