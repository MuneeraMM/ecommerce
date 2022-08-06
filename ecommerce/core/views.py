from itertools import product
from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from core.forms import *
from core.models import *
from django.utils import timezone
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

def add_to_cart(request,pk):
    # Get that particular product of id = pk
    product = Product.objects.get(pk=pk)
    # Create Order item
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )

    # Get query set of order object of particular user
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"Added quantity item")
            return redirect("product_desc",pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"Item added to cart")
            return redirect("product_desc",pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item added to cart")
        return redirect("product_desc",pk=pk)

def orderlist(request):
    if Order.objects.filter(user=request.user,ordered=False).exists():
        order = Order.objects.get(user = request.user,ordered=False)
        return render(request,'core/orderlist.html',{'order':order})
    return render(request,'core/orderlist.html',{'message':"Your cart is empty"})

def add_item(request,pk):
    # Get that particular product of id = pk
    product = Product.objects.get(pk=pk)
    # Create Order item
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )

    # Get query set of order object of particular user
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity +=1
                order_item.save()
                messages.info(request,"Added quantity item")
                return redirect("orderlist")
            else:
                messages.info(request,"Sorry! Product is out of stock")
                return redirect("orderlist")
        else:
            order.items.add(order_item)
            messages.info(request,"Item added to cart")
            return redirect("product_desc",pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item added to cart")
        return redirect("product_desc",pk=pk)

def remove_item(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user = request.user,
                ordered = False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request,"Item quantity was updated")
            return redirect("orderlist")
        else:
            messages.info(request,"This item is not in your cart")
            return redirect("orderlist")
    else:
        messages.info(request,"You do not have any order")
        return redirect("orderlist")

def checkout_page(request):
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request, 'core/checkout_address.html',{'payment_allow':"allow"})
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        try:
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip')
                checkout_address = CheckoutAddress(
                    user = request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip_code= zip_code,
                )
                checkout_address.save()
                print("It should render the summary page")
                return render(request, 'core/checkout_address.html',{'payment_allow':"allow"})
        except Exception as e:
            messages.warning(request, "Failed checkout")
            return redirect('checkout_page')
    else:
        form = CheckoutForm()
        return render(request, 'core/checkout_address.html', {'form': form})
