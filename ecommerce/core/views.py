from django.contrib import messages
from django.shortcuts import render,redirect
from core.forms import *

# Create your views here.
def index(request):
    return render(request,'core/index.html')

def add_product(request):
    if request.method == 'POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            print("True")
            form.save()
    
            print("Data saved successfully")
            return redirect('add_product')
        else:
            print("Not working")
            messages.info(request,"Product is not added, try again")
    else:
        print("form not valid")
        form = ProductForm()
    return render(request, "core/add_product.html", {'form':form})