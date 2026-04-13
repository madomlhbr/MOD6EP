from django.db import models
from django.utils import timezone

class Supplier(models.Model): 
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()

    def getName(self):
        return self.name

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country} created at: {self.created_at}"

class WaterBottle(models.Model):
    sku =  models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    mouth_size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    supplied_by = models.ForeignKey(Supplier, on_delete=models.CASCADE) 
    current_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.sku}: {self.brand}, {self.mouth_size}, {self.size}, {self.color}, supplied by {self.supplied_by.name}, {self.cost} : {self.current_quantity}"
    
class Account(modules.Model):
    username = models.CharField(max_length=50, unique = True)
    password = models.CharField(max_length=50)

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    