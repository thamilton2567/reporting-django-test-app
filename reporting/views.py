from django.shortcuts import render
from .models import Business
from django.db.models import Sum
from .forms import FilterForm

# Create your views here.
def index(request):
  
  customers = Business.objects.all() \
              .annotate(total_job_line_item_amount=Sum("jobs__lineitem__amount")) \
              .annotate(total_job_line_item_amount_remaining_to_be_invoiced=(Sum("jobs__lineitem__amount")-Sum('jobs__lineitem__invoiceditem__amount'))) \
              .annotate(total_invoice_line_item_amount=Sum("invoices__lineitem__amount")) \
              .order_by('-total_job_line_item_amount_remaining_to_be_invoiced', 'name')
              
  if request.method == "POST":
      #Get the posted form
      MyDataForm = FilterForm(request.POST)
      
      if MyDataForm.is_valid():
        min = MyDataForm.cleaned_data['min']
        max = MyDataForm.cleaned_data['max']
        if max > min:
          customers = customers.filter(total_job_line_item_amount_remaining_to_be_invoiced__gt=min, total_job_line_item_amount_remaining_to_be_invoiced__lt=max)
  
  context = {
    "customers": customers
  }
  return render(request, "index.html", context)
