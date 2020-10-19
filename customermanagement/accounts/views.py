from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.shortcuts import render
from .models import *
from .forms import *
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group



def logoutuser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def loginpage(request):
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)

            if user is not  None:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.info(request,'Username or password is incorrect')
                return render(request, 'accounts/login.html')

        return  render(request,'accounts/login.html')

@unauthenticated_user
def registerPage(request):

            f = CreateUserForm()
            if request.method == 'POST':
                form = CreateUserForm(request.POST)
                print("IN here")
                if form.is_valid():
                    print("form is valid")
                    u = form.save()
                    #grp = Group.objects.get(name='customer')
                    #u.groups.add(grp)
                    user = form.cleaned_data['username']
                    #email = form.cleaned_data['email']
                    #Customer.objects.create(
                        #user=u,
                        #name=user,
                        #email=email,
                        #phone="",
                    #)
                    messages.success(request, 'Account Creation is Successful!!' + user)
                    return redirect('login/')
                else:
                    print("Not accepting")

            context = {"form": f}

            print("First")
            return render(request, 'accounts/register.html', context)

# Create your views here.
@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    order=customer.orders_set.all() #accessing the child set that is orders is child of customer
    order_cnt=customer.orders_set.all().count()
    myfilter=OrderFilter(request.GET,queryset=order)
    order=myfilter.qs

    context={'customer':customer,'order':order,'count':order_cnt,'myfilter':myfilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def products(request):
    product=Products.objects.all()
    return render(request,'accounts/products.html',{'products':product})

@login_required(login_url='login/')
@admin_only
def dashboard(request):
    customer = Customer.objects.all()
    order = Orders.objects.all()
    total_orders=Orders.objects.all().count()
    total_delivered=Orders.objects.filter(status='delivered').count()
    total_pending=Orders.objects.filter(status='Pending').count()
    context = {'customers': customer, 'orders': order,'total_order':total_orders,'total_del':total_delivered,'total_pen':total_pending}
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def orderform(request):     #create order for registerd customers
    context={}

    form=orderForm()
    if request.method == 'POST':
        form=orderForm(request.POST)
        if form.is_valid():
            print('form valid')
            form.save()
            return redirect('dashboard')



    context['form']=form
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def updateform(request,pk):         #update order which is already placed by customer
    context = {}
    order=Orders.objects.get(id=pk)
    form=orderForm(instance=order)
    context={'form':form}
    if request.method=="POST":
        form = orderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request,pk):
    order=Orders.objects.get(id=pk)
    context={"name":order.customer.name,"item":order.product.name}
    if request.method=="POST":
        order.delete()
        return redirect('dashboard')
    return render(request,'accounts/deleteorder.html',context)

@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def createcustomer(request):
    context={}

    if request.method=="POST":
        form=customerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    form=customerForm()
    context['form']=form

    return render(request,'accounts/createcustomer.html',context)

@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def updatecustomer(request,pk):
    customer=Customer.objects.get(id=pk)
    form=customerForm(instance=customer)
    context = {"form":form}

    if request.method=="POST":
        form=customerForm(request.POST,instance=customer)
        context["form"]=form
        if form.is_valid():
            form.save()
            return redirect('dashboard')



    return render(request,'accounts/updatecustomer.html',context)

@login_required(login_url='login/')
@allowed_users(allowed_roles=['admin'])
def deletecustomer(request,pk):

    context={}

    customer=Customer.objects.get(id=pk)

    context["name"]=customer.name

    if request.method=="POST":
        customer.delete()
        return redirect('dashboard')

    return  render(request,'accounts/deletecustomer.html',context)

@login_required(login_url='login/')
def orderspecific(request,pk):

    customer=Customer.objects.get(id=pk)
    name=customer.name

    formset=formset_factory(Orders)
    form=formset(request.POST)
    #form=orderForm()
    context={"form":form,"name":name}

    if request.method=="POST":
        if form.is_valid():
            for f in form:
                f.save()
            return  redirect('dashboard')

    return render(request,'accounts/orderspecific.html',context)
@login_required(login_url='login/')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders_of_user=request.user.customer.orders_set.all()
    total_orders=orders_of_user.count()
    total_delivered=orders_of_user.filter(status='Delivered').count()
    total_pending=orders_of_user.filter(status='Pending').count()
    print(orders_of_user)

    context = {'order':orders_of_user,'total_order':total_orders,'total_del':total_delivered,'total_pen':total_pending}

    return render(request,'accounts/userpage.html',context)

@login_required(login_url='login/')
@allowed_users(allowed_roles=['customer'])
def accounts_settings(request):
    u=request.user.customer
    form=customerForm(instance=u)
    if request.method=='POST':
        form=customerForm(request.POST,request.FILES,instance=u)
        if form.is_valid():
            form.save()


    context={'form':form}
    return render(request,'accounts/account.html',context)













