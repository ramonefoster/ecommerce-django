from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cartData, guestOrder

# Create your views here.
def store(request):
    data = cartData(request)  
    cart_items = data['cart_items']
        
    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items}
    return render(request, "store/store.html", context)

def cart(request):
    #Check if user is is_authenticated
    data = cartData(request)  
    cart_items = data['cart_items']
    items = data['items']
    order = data['order']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, "store/cart.html", context)

def checkout(request):  
    data = cartData(request)  
    cart_items = data['cart_items']
    items = data['items']
    order = data['order']
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, "store/checkout.html", context)

def updateItem(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    print(product_id, action)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
    else:
        customer, order = guestOrder(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    
    order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order = order,
                address = data['shipping']['address'],
                zipcode = data['shipping']['zipcode'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
            )

    return JsonResponse('Payment Complete!', safe=False)