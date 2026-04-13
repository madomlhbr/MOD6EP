from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Account, Supplier, WaterBottle


def get_current_account(request):
    account_id = request.session.get('account_id')
    if account_id:
        try:
            return Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            pass
    return None


def login_view(request):
    message = ""
    message_type = "danger"

    if request.GET.get("created") == "true":
        message = "Account created successfully"
        message_type = "success"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        account = Account.objects.filter(username=username, password=password).first()
        if account:
            request.session['account_id'] = account.pk
            return redirect('view_supplier')

        message = "Invalid login"
        message_type = "danger"

    return render(request, "MyInventoryApp/login.html", {
        "message": message,
        "message_type": message_type,
    })


def signup_view(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if Account.objects.filter(username=username).exists():
            message = "Account already exists"
        else:
            Account.objects.create(username=username, password=password)
            return redirect(f"{reverse('login')}?created=true")

    return render(request, "MyInventoryApp/signup.html", {"message": message})


def view_supplier(request):
    suppliers = Supplier.objects.all()
    account = get_current_account(request)
    return render(request, "MyInventoryApp/view_supplier.html", {"suppliers": suppliers, "account": account})


def view_bottles(request, pk):
    if pk == -1:
        bottles = WaterBottle.objects.all()
    else:
        bottles = WaterBottle.objects.filter(Supplier = pk)
    return render(request, "MyInventoryApp/bottle_list.html", {"bottles": bottles})


def view_bottle_details(request, pk):
    bottle = get_object_or_404(WaterBottle, pk=pk)

    if request.method == "POST":
        WaterBottle.objects.filter(pk=pk).delete()
        return redirect('view_bottles')

    return render(request, "MyInventoryApp/view_bottle_details.html", {"bottle": bottle})

def add_bottle(request):
    suppliers = Supplier.objects.all()
    errors = []
    form_data = {
        "sku": "",
        "brand": "",
        "cost": "",
        "size": "",
        "mouth_size": "",
        "color": "",
        "supplied_by": "",
        "current_quantity": "",
    }

    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('view_supplier')

        form_data = {
            "sku": request.POST.get("sku", "").strip(),
            "brand": request.POST.get("brand", "").strip(),
            "cost": request.POST.get("cost", "").strip(),
            "size": request.POST.get("size", "").strip(),
            "mouth_size": request.POST.get("mouth_size", "").strip(),
            "color": request.POST.get("color", "").strip(),
            "supplied_by": request.POST.get("supplied_by", ""),
            "current_quantity": request.POST.get("current_quantity", "").strip(),
        }

        sku = form_data["sku"]
        brand = form_data["brand"]
        cost_value = form_data["cost"]
        size = form_data["size"]
        mouth_size = form_data["mouth_size"]
        color = form_data["color"]
        supplied_by_id = form_data["supplied_by"]
        current_quantity_value = form_data["current_quantity"]

        if not sku:
            errors.append("SKU is required.")
        elif WaterBottle.objects.filter(sku=sku).exists():
            errors.append("A bottle with that SKU already exists.")

        if not brand:
            errors.append("Brand is required.")

        if not cost_value:
            errors.append("Cost is required.")
        else:
            try:
                cost = Decimal(cost_value)
                if cost < 0:
                    errors.append("Cost cannot be negative.")
            except InvalidOperation:
                errors.append("Cost must be a valid number.")

        if not mouth_size:
            errors.append("Mouth size is required.")

        if not color:
            errors.append("Color is required.")
        
        if not size:
            errors.append("Size is required.")


        if not current_quantity_value:
            errors.append("Quantity is required.")
        else:
            try:
                current_quantity = int(current_quantity_value)
                if current_quantity < 0:
                    errors.append("Quantity cannot be negative.")
            except ValueError:
                errors.append("Quantity must be an integer.")

        supplier = None
        if supplied_by_id:
            supplier = Supplier.objects.filter(pk=supplied_by_id).first()
            if not supplier:
                errors.append("Supplier selection is invalid.")
        else:
            errors.append("Supplier selection is required.")

        if not errors:
            WaterBottle.objects.create(
                sku=sku,
                brand=brand,
                cost=cost,
                size=size,
                mouth_size=mouth_size,
                color=color,
                supplied_by=supplier,
                current_quantity=current_quantity
            )
            return redirect('view_supplier')

    return render(request, "MyInventoryApp/add_bottle.html", {
        "suppliers": suppliers,
        "errors": errors,
        **form_data,
    })

def logout_view(request):
    request.session.flush()
    return redirect('login')


def delete_account(request, pk):
    Account.objects.filter(pk=pk).delete()
    request.session.flush()
    return redirect('login')


def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, "MyInventoryApp/manage_account.html", {"account": account})


def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    message = ""

    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('manage_account', pk=account.pk)

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if current_password == account.password and new_password == confirm_password:
            account.password = new_password
            account.save()
            return redirect('manage_account', pk=account.pk)
        else:
            message = "Password change failed"

    return render(request, "MyInventoryApp/change_password.html", {
        "account": account,
        "message": message
    })


