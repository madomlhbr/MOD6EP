from django.shortcuts import render, redirect
from .models import WaterBottle, Supplier, Account

# Create your views here.
def get_current_account(request):
    account_id = request.session.get('account_id')
    if account_id:
        try:
            return Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            pass
    return None

def view_supplier(request):
    suppliers = Supplier.objects.all() 
    return render(request, 'MyInventoryApp/view_supplier.html', {'suppliers': suppliers})

def view_bottles(request):
    bottles = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottles})

def add_bottle(request):
    return render(request, 'MyInventoryApp/add_bottle.html')

def login_view(request):
    error_message = None

    if request.method == "POST":
        user_input = request.POST.get('username')
        pass_input = request.POST.get('password')
        
        try:
            user = Account.objects.get(username=user_input, password=pass_input)
            return redirect('view_supplier')
        except Account.DoesNotExist:
            error_message = "Invalid login"
            
    return render(request, 'MyInventoryApp/login.html', {'error': error_message})