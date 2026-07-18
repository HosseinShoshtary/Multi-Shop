from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart_madule import Cart
from product.models import Product


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, template_name="cart/cart_detail.html", context={"cart": cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size, color, quantity = request.POST.get("size", "empty"), request.POST.get("color", "empty"), request.POST.get("quantity")
        print(size,color,quantity)
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect("cart:cart_detail")


class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect("cart:cart_detail")
