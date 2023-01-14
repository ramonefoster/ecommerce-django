from django.urls import path, include
from . import views

urlpatterns = [
    path("", view=views.store, name="store"), 
    path("cart", view=views.cart, name="cart"), 
    path("checkout", view=views.checkout, name="checkout"), 
]
