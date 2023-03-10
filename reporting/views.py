from django.shortcuts import render
from .models import Business, Job, Invoice
from django.db.models import Sum, Exists, OuterRef
from .forms import FilterForm
from django.contrib import messages

# Create your views here.
def index(request):
  
  customers = Business.objects.filter(Exists(Job.objects.filter(business=OuterRef('id')))) \
              .annotate(total_job_line_item_amount=Sum("jobs__lineitem__amount"),
                total_job_line_item_amount_remaining_to_be_invoiced=(Sum("jobs__lineitem__amount")-Sum('jobs__lineitem__invoiceditem__amount')),
                total_invoice_line_item_amount=Sum('jobs__lineitem__invoiceditem__amount')
              ).order_by('-total_job_line_item_amount_remaining_to_be_invoiced', 'name')
              
  if request.method == "POST":
    #Get the posted form
    MyDataForm = FilterForm(request.POST)
    
    if MyDataForm.is_valid():
      min = MyDataForm.cleaned_data['min']
      max = MyDataForm.cleaned_data['max']
      if max > min:
        customers = customers.filter(total_job_line_item_amount_remaining_to_be_invoiced__gt=min, total_job_line_item_amount_remaining_to_be_invoiced__lt=max)
      else:
        messages.warning(request, 'Maximum value should be greater than minimum value')
  
  for customer in customers:
    customer_all_invoiced_items = Invoice.objects.filter(lineitem__self_item__job__business=customer).distinct()
    customer.invoice_lists = customer_all_invoiced_items    
  
    payments = customer.payments_sent.all().values("payment_type", "reference").annotate(amount_sum=Sum('amount')).order_by('payment_type', 'reference')
    customer.payment_lists = payments

  context = {
    "customers": customers
  }
  return render(request, "index.html", context)
