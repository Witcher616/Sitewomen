from django.contrib.auth.models import Group


def new_user_handler(backend, user, response, *args, **kwargs):
    group = Group.objects.filter(name='social')
    if len(group):
        user.groups.add(group[0])
