from django.db import models
from django.contrib.auth.models import User

INSTITUTION_TYPE = (
    (1, "Charitable foundation"),
    (2, "Non-governmental organisation"),
    (3, "Local fund-raiser")
)

class Category(models.Model):
    name = models.CharField(max_length=30)

class Institution(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTION_TYPE, default=1)
    categories = models.ManyToManyField(Category)

class Donation(models.Model):
    quantity = models.FloatField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.IntegerField(max_length=13)
    zip_code = models.IntegerField(max_length=8)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=80)
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
