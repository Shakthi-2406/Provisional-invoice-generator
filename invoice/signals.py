from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .models import Invoice,Order
from django.db.models.signals import post_save, pre_save
from .forms import InvoiceForm, OrderForm
from django.dispatch import receiver
from django.forms import BaseFormSet


@receiver(pre_save, sender=Order)
def order_save_calculate_amount(sender, instance, *args, **kwargs):
    if instance.amount == None:
        p = instance.price + ((0.01*instance.tax)*instance.price)
        instance.amount = int(p*instance.quantity)
        instance.save()
