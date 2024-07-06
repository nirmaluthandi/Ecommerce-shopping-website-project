from django.http import JsonResponse
from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json
# Create your views here.
def Home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'shop/index.html',{"products":products})

def Add_to_Cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authentication:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                 if Cart.objects.filter(user=request.user.id,product_id=product_id):
                     return JsonResponse({'status':'Product Already in Cart'},status=200)
                 else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)   
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def Login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Login Successfully")
                return redirect('/')
            else:
                messages.error(request,"invalid user name or password")
                return redirect('/login')
        return render(request,'shop/login.html')

def Logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout Successfully")
        return redirect("/")


def Register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Login Now...!")
            return redirect('/login/')
    return render(request,'shop/register.html',{'form':form})

def Collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,'shop/collections.html',{'catagory':catagory})

def Collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catagory__name=name)
        return render(request,'shop/products/index.html',{'products':products,"category__name":name})
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect('collections')

def Product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{"products":products})
        else:
            messages.error(request,"NO Such Product Found")
            return redirect('collections')
    else:
        messages.error(request,"NO Such Category Found")
        return redirect('collections')


