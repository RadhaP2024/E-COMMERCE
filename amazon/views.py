from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from .forms import RegisterForm, CheckoutForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    cart[id] = cart.get(id, 0) + 1

    request.session['cart'] = cart
    return redirect('viewcart')


def viewcart(request):
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
    return redirect('viewcart')


def decrease(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        if cart[id] > 1:
            cart[id] -= 1
        else:
            del cart[id]

    request.session['cart'] = cart
    return redirect('viewcart')


def remove(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        del cart[id]

    request.session['cart'] = cart
    return redirect('viewcart')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    total = 0

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():

            order = Order.objects.create(
                user=request.user,
                total_amount=0
            )

            for id, quantity in cart.items():
                product = get_object_or_404(Product, id=int(id))
                total += product.price * quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

            order.total_amount = total
            order.save()

            request.session['cart'] = {}

            return redirect('product_list')
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form})
