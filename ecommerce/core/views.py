from django.contrib import messages
from django.shortcuts import render,redirect
from core.forms import *

# Create your views here.
def index(request):
    # to get all products from database table
    products = Product.objects.all()
    return render(request,"core/index.html",{'products':products})

    

def add_product(request):
    if request.method == 'POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            print("True")
            form.save()
    
            print("Data saved successfully")
            messages.success(request,"Product added successfully")

            return redirect('/')
        else:
            print("Not working")
            messages.info(request,"Product is not added, try again")
    else:
        print("form not valid")
        form = ProductForm()
    return render(request, "core/add_product.html", {'form':form})

def product_desc(request,pk):
    # Get that particular product of id = pk
    product = Product.objects.get(pk=pk)
    return render(request,'core/product_desc.html',{'product':product})