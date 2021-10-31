from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"{self.name}"


CHOICES = [
        ('fundation', "Fundacja"),
        ('NGO', 'Organizacja pozarządowa'),
        ('localy', 'Zbiórka lokalna'),
    ]
class Institution(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    type = models.CharField(choices=CHOICES, default='fundation',max_length=64, null=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.categories.name}"

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    adress = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=32)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField(auto_now_add=True, null=True)
    pick_up_time = models.TimeField(auto_now_add=True, null=True)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(CustomUser, null=True, default=None, on_delete=models.SET_NULL)
    is_taken = models.BooleanField(default=False)