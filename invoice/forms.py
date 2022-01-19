from django.forms import ModelForm, fields,models
from .models import Invoice,Order
from django import forms


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        # fields = ['s_name',]
        fields = ['s_name','s_address','s_phone','b_name','b_address','b_phone',]

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name','price','tax','quantity','delete_it']