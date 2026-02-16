from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_details.html', {'product': product})

def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    id = str(id)  # store keys as strings
    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1

    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    final_amount = 0

    for id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(id))
        total = product.price * quantity
        final_amount += total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'final_amount': final_amount
    })

def increase(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        cart[id] += 1

    request.session['cart'] = cart
    return redirect('view_cart')

def decrease(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        if cart[id] > 1:
            cart[id] -= 1
        else:
            del cart[id]

    request.session['cart'] = cart
    return redirect('view_cart')

def remove(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        del cart[id]

    request.session['cart'] = cart
    return redirect('view_cart')
