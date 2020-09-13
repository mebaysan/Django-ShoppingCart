from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Product
from cart.cart import Cart


def index(request):
    username = request.session.get('username')  # session'daki değeri alır (get)
    products = Product.objects.all()
    context = {
        # 'username': username
        'products': products,
    }
    return render(request, 'index.html', context=context)


def deneme(request):
    request.session['username'] = 'mebaysan'  # session'a değer ekler (set)
    # del request.session['username'] # session'dan ilgili değeri siler (del)
    return redirect('index')


def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product,
             quantity=1,
             override_quantity=False)
    return redirect('index')


def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('index')


def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'detail.html', context=context)
