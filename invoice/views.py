from fileinput import filename
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
import locale
locale.setlocale(locale.LC_MONETARY,'en_IN')


def create_order(request,*args, **kwargs):
    if Invoice.objects.all():
        addx = Invoice.objects.all().last().id
    else:
        addx = 0
    pk_list = []
    for i in reversed(range(1,addx+1)):
        pk_list.append(i)
    if request.method == 'POST':
        invoice = InvoiceForm(request.POST)

        OrderFormSet = formset_factory(OrderForm)
        order_formset = OrderFormSet(request.POST)

        if order_formset.is_valid() and invoice.is_valid():
            invoice.save()
            new_orders = []
            new_order = []
            for order_form in order_formset:
                if order_form.cleaned_data.get("delete_it") != True:
                    new_order = Order(
                        ordered = invoice.instance,
                        price = order_form.cleaned_data.get("price"),
                        render_price = locale.currency(order_form.cleaned_data.get("price"),grouping=True)[2:],
                        name = order_form.cleaned_data.get("name").capitalize(),
                        tax = order_form.cleaned_data.get("tax"),
                        delete_it = order_form.cleaned_data.get("delete_it"),
                        quantity = order_form.cleaned_data.get("quantity"),
                        amount = round(float((order_form.cleaned_data.get("price")+((0.01*order_form.cleaned_data.get("tax"))*order_form.cleaned_data.get("price")))*order_form.cleaned_data.get("quantity")),2),
                    )
                    new_orders.append(new_order)
            Order.objects.bulk_create(new_orders)
            invoice_form = InvoiceForm()
            OrderFormSet= formset_factory(OrderForm, extra=1)
            order_formset = OrderFormSet()
            return redirect('finale', pk=invoice.instance.id )
            # return redirect('admin/')
    if request.method == 'GET':
        invoice_form = InvoiceForm()
        OrderFormSet= formset_factory(OrderForm, extra=1)
        order_formset = OrderFormSet()
        return render(request, 'die.html', {'invoice_form':invoice_form, 'addx':addx+1,'pk_list':pk_list, 'order_formset':order_formset})



def invoiceFun(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    all_items = invoice.orderline.all()
    y = ("000"+str(pk))[-4:]
    name = f"Invoice{y}"
    download = False

    return convert_to_pdf(request,'check.html', {
        'name': name,
        'invoice': invoice,
        'all_items': all_items
    }, name, download)



def final(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    all_items = invoice.orderline.all()
    x = 0
    numbering = 1
    for item in all_items:
        x += item.amount
        item.num = numbering
        item.render_amount = locale.currency(item.amount,grouping=True)[2:]
        item.save()
        numbering += 1

    invoice.total = round(x,2)
    invoice.render_total = locale.currency(round(x,2),grouping=True)[2:]
    invoice.save()
    y = ("000"+str(pk))[-4:]
    name = f"Invoice{y}"
    download = True

    return convert_to_pdf(request,'check.html', {
        'name': name,
        'invoice': invoice,
        'all_items': all_items
    }, name, download)



def convert_to_pdf(request,template_src, context_dict, name, download):
    template = get_template(template_src)
    context = context_dict
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(src=BytesIO(html.encode("ISO-8859-1")),dest= result)
    filename = f'{name}.pdf'
    converted = result.getvalue() if not pdf.err else ''
    response = HttpResponse(result.getvalue(),content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s' %filename

    if download:
        response['Content-Disposition'] = 'attachment; filename=%s' %filename
    response.write(converted)
    # pyautogui.hotkey('f5')

    if not pdf.err:
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))






















































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