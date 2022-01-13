from django.contrib import admin
from .models import Invoice,Order

# Register your models here.


class OrderInLineAdmin(admin.TabularInline):
    model = Order

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [OrderInLineAdmin]

admin.site.register(Invoice,InvoiceAdmin)