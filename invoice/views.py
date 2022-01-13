from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, HttpResponseRedirect
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from html import escape
from .models import Invoice,Order
from django.db.models.signals import post_save, pre_save
from .forms import InvoiceForm, OrderForm


def create_order(request,*args, **kwargs):
    addx = []
    if request.method == 'POST':
        invoice = InvoiceForm(request.POST)
        if invoice.is_valid():
            invoice.save()
        
        OrderFormSet = formset_factory(OrderForm)
        order_formset = OrderFormSet(request.POST)

        if order_formset.is_valid() and invoice.is_valid():
            new_orders = []
            for order_form in order_formset:
                new_order = Order(
                    ordered = invoice.instance,
                    price = order_form.cleaned_data.get("price"),
                    name = order_form.cleaned_data.get("name"),
                    tax = order_form.cleaned_data.get("tax"),
                    quantity = order_form.cleaned_data.get("quantity"),
                    amount = int((order_form.cleaned_data.get("price")+((0.01*order_form.cleaned_data.get("tax"))*order_form.cleaned_data.get("price")))*order_form.cleaned_data.get("quantity")),
                )
                new_orders.append(new_order)
            Order.objects.bulk_create(new_orders)
            print(invoice.instance.id)
            return redirect('finale', pk=invoice.instance.id )
            # return redirect('admin/')
    if request.method == 'GET':
        invoice_form = InvoiceForm()
        OrderFormSet= formset_factory(OrderForm, extra=1)
        order_formset = OrderFormSet()
        return render(request, 'die.html', {'invoice_form':invoice_form, 'addx':addx, 'order_formset':order_formset})



def final(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    all_items = invoice.orderline.all()
    x = 0
    numbering = 1
    for item in all_items:
        x += item.amount
        item.num = numbering
        item.save()
        numbering += 1
    invoice.total = x
    invoice.save()
    y = ("00"+str(pk))[-3:]
    name = f"Invoice{y}"
    conktext={
        'name': name,
        'invoice': invoice,
        'all_items': all_items,
        'pagesize':'A4',
    }
    # return render(request, 'xxx.html', conktext)
    return render_to_pdf('xxx.html', {
        'name': name,
        'invoice': invoice,
        'all_items': all_items,
        'pagesize':'A4',
    })





def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = context_dict
    html  = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))







# @receiver(pre_save, sender=Order)
# def order_save_calculate_price(sender, instance, raw, using, update_fields, **kwargs):
#     print(sender)
#     instance.amount = (instance.price*(1+instance.tax))*instance.quantity
#     instance.save()
#     print("Success!!!")














































# class RequiredFormSet(BaseFormSet):
#     def add_form(self, **kwargs):
#         # add the form
#         tfc = self.total_form_count()
#         self.forms.append(self._construct_form(tfc, **kwargs))
#         self.forms[tfc].is_bound = False

#         # make data mutable
#         self.data = self.data.copy()

#         # increase hidden form counts
#         total_count_name = '%s-%s' % (self.management_form.prefix, TOTAL_FORM_COUNT)
#         initial_count_name = '%s-%s' % (self.management_form.prefix, INITIAL_FORM_COUNT)
#         self.data[total_count_name] = self.management_form.cleaned_data[TOTAL_FORM_COUNT] + 1
#         self.data[initial_count_name] = self.management_form.cleaned_data[INITIAL_FORM_COUNT] + 1

#     def add_fields(self, form, index):
#         super(RequiredFormSet, self).add_fields(form, index)
#         form.empty_permitted = False