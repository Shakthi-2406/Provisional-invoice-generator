from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class Invoice(models.Model):
    s_name = models.CharField(max_length=100, null=False)
    s_address = models.TextField(null=False)
    s_phone = models.CharField(max_length=13,null=False)
    b_name = models.CharField(max_length=100, null=False)
    b_address = models.TextField(null=False)
    b_phone = models.CharField(max_length=15,null=False)
    total = models.PositiveIntegerField(blank=True,null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"INVOICE00{self.id}"

class Order(models.Model):
    price = models.PositiveIntegerField(blank=False,null=False)
    amount = models.PositiveIntegerField(blank=True,null=True)
    tax = models.FloatField(null=False)
    name = models.CharField(max_length=100, null=False)
    quantity = models.PositiveIntegerField(default=1, null=False)
    num = models.PositiveIntegerField(null=True,blank=True)
    ordered = models.ForeignKey(Invoice,related_name='orderline',on_delete=CASCADE)


    def __str__(self):
        return self.name