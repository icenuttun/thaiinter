from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_editor = models.BooleanField(default=False)
    is_adder = models.BooleanField(default=False)

    # add related_name arguments to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_set', blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )