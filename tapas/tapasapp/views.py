from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish 
from .models import Account

from django.contrib import messages # Jaysha. (2020, June 3). How to use Django Messages Framework. Ordinary Coders. https://ordinarycoders.com/blog/article/django-messages-framework

# Create your views here.

def login_page(request):
    if(request.method=="POST"):
        usernameLogin = request.POST.get("username_")
        passwordLogin = request.POST.get("password_")
        try:
            accountNo = Account.objects.get(username=usernameLogin, password=passwordLogin)
            return redirect('better_menu', pk=accountNo.pk)  # kushtrimh. (2018, March 9). What is the difference render() and redirect() in Django? Stack Overflow. https://stackoverflow.com/questions/39930414/what-is-the-difference-render-and-redirect-in-django#:~:text=The%20render%20function%20Combines%20a,9262%2014%2033      
        except:
            messages.error(request, "Invalid login") # Sj. (n.d.). Python/Django: How to display error messages on invalid login? Stack Overflow. https://stackoverflow.com/questions/47923952/python-django-how-to-display-error-messages-on-invalid-login-->
            return render(request, 'tapasapp/login_page.html')
    else:
        return render(request, 'tapasapp/login_page.html')

def signup_page(request):
    if(request.method=="POST"):
        usernameNew = request.POST.get("username_")
        passwordNew = request.POST.get("password_")
        accounts_checker = Account.objects.filter(username=usernameNew)
        if accounts_checker:
            messages.error(request,"Account already exists")
            return render(request, 'tapasapp/signup_page.html')
        else:
            Account.objects.create(username=usernameNew, password=passwordNew)
            messages.success(request,"Account created successfully")
            return redirect('login_page')
    else:
        return render(request, 'tapasapp/signup_page.html')
    
def manage_account(request, pk):
    accountNo = get_object_or_404(Account,pk=pk)
    if(request.method=="POST"):
        if "change_password" in request.POST: # Seb-furn. (2020). How to check the name of a button clicked in a post form? Reddit. https://www.reddit.com/r/django/comments/eplphj/how_to_check_the_name_of_a_button_clicked_in_a/
            return redirect('change_password', pk=accountNo.pk)
        elif "delAccount" in request.POST:
            messages.info(request,"You deleted your account!")
            Account.objects.get(pk=accountNo.pk).delete()
            return redirect('login_page')
        elif "goBackfromMA" in request.POST:
            return redirect('better_menu', pk=accountNo.pk)
    return render(request, 'tapasapp/manage_account.html', {'accountNo':accountNo})

def change_password(request, pk):
    accountNo = get_object_or_404(Account,pk=pk)
    passwordOld= request.POST.get("passwordOLD")
    passwordNew= request.POST.get("password_")
    passwordConfirm = request.POST.get("passwordCONFIRM")
    if(request.method=="POST"):
        if "submitNewPassword" in request.POST:
            if passwordOld == accountNo.password and passwordNew == passwordConfirm:
                Account.objects.filter(pk=accountNo.pk).update(password=passwordNew)
                accountNo.password = passwordNew
                messages.success(request,"Password changed successfully")
                return redirect('manage_account', pk=accountNo.pk)
            else:
                messages.error(request,"Unsuccessful. Try again.")
                return render(request, 'tapasapp/change_password.html', {'accountNo':accountNo})
        elif "goBackfromCP" in request.POST:
            return redirect('manage_account', pk=accountNo.pk)
    return render(request, 'tapasapp/change_password.html', {'accountNo':accountNo})

def better_menu(request, pk):
    if(request.method=="POST"):
        accountNo = get_object_or_404(Account,pk=pk)
        return redirect('manage_account', pk=accountNo.pk)  
    else:
        accountNo = get_object_or_404(Account,pk=pk)
        dishes = Dish.objects.all()
        return render(request, 'tapasapp/better_list.html', {'accountNo':accountNo, 'dishes': dishes})

def add_menu(request):
    if(request.method=="POST"):
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')

def update_dish(request, pk):
    if(request.method=="POST"):
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d':d})