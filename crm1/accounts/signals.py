from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
    """create and a user to the group customer"""
    if created:
        group = Group.objects.get(name='customer')
        print("group", group)
        instance.groups.add(group) # add the user "instance" to the group custome
        # associate as a customer
        Customer.objects.create(
            user=instance,
            name=instance.username
            )
        print("profile created!!")

post_save.connect(customer_profile, sender=User)
