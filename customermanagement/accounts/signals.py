from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group

def create_customer(sender,instance,created,**kwargs):
    if created:
        grp = Group.objects.get(name='customer')
        instance.groups.add(grp)

        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
            phone="123456789",
        )
        print('Profile created')

post_save.connect(create_customer,sender=User)