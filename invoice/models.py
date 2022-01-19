from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class Invoice(models.Model):
    s_name = models.CharField(max_length=100, null=False)
    s_address = models.TextField(null=True)
    s_phone = models.CharField(max_length=13,null=True)
    b_name = models.CharField(max_length=100, null=True)
    b_address = models.TextField(null=True)
    b_phone = models.CharField(max_length=15,null=True)
    total = models.FloatField(blank=True,null=True)
    render_total = models.CharField(max_length=200,blank=True,null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"INVOICE00{self.id}"

class Order(models.Model):
    price = models.FloatField(blank=False,null=False)
    render_price = models.CharField(max_length=200,blank=True,null=True)
    amount = models.FloatField(blank=True,null=True)
    render_amount = models.CharField(max_length=200,blank=True,null=True)
    tax = models.FloatField(null=False, default=1.8)
    name = models.CharField(max_length=100,null=False)
    quantity = models.PositiveIntegerField(default=1, null=False)
    num = models.PositiveIntegerField(null=True,blank=True)
    ordered = models.ForeignKey(Invoice,related_name='orderline',on_delete=CASCADE)
    delete_it = models.BooleanField(default=False,blank=True,null=True)


    def __str__(self):
        return self.name