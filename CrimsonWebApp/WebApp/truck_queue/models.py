from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Table schemas go below. As of now, I'm just going with whatever I can think of
# We should talk about the database organization and what data we need to store
class Truck(models.Model):
    truck_name = models.CharField(max_length=200)
    truck_description = models.CharField(max_length=1000)
    truck_day = models.CharField(max_length=9, default='Every day')

    def __unicode__(self):
        return self.truck_name


class MenuItems(models.Model):
    truck = models.ForeignKey(Truck)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    is_gluten_free = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_side = models.BooleanField(default=False)
    is_extra = models.BooleanField(default=False)
    is_protein = models.BooleanField(default=False)

    def __unicode__(self):
        return "{0}: {1}".format(self.truck.truck_name, self.name)


class Order(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    menu_item = models.OneToOneField(MenuItems)
    item_count = models.IntegerField()


class Rating(models.Model):
    menu_item = models.ForeignKey(MenuItems)
    user = models.OneToOneField(User)
    stars = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    date = models.DateField()


class Employee(models.Model):
    username = models.OneToOneField(User)
    activation_number = models.IntegerField()
    phone = models.IntegerField()
    strikes = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.username)

class OpenOrders(models.Model):
    number = models.IntegerField
    username = models.CharField(max_length=200)

    def __unicode__(self):
        return self.number
