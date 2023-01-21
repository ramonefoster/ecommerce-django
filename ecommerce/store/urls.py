from django.urls import path, include
from . import views

urlpatterns = [
    path("", view=views.store, name="store"), 
    path("cart/", view=views.cart, name="cart"), 
    path("checkout/", view=views.checkout, name="checkout"), 
    path("update_item/", view=views.updateItem, name="update_item"), 
    path("process_order/", view=views.processOrder, name="process_order"), 
]
