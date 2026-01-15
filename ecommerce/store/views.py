from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import razorpay

from .models import Product, Category, CartItem, Order


# --------------------
# RAZORPAY CLIENT
# --------------------
#client = razorpay.Client(
 #   auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
#)


# --------------------
# HOME PAGE
# --------------------
def home(request):
    search = request.GET.get('search')
    category_id = request.GET.get('category')

    products = Product.objects.all()
    categories = Category.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'store/index.html', {
        'products': products,
       'categories': categories
    })
    

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {
        'product': product
    })
# --------------------
# AUTH
# --------------------
def register(request):
    form = UserCreationForm(request.POST or None)

    # ADD BOOTSTRAP CLASSES
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})

    if form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'store/register.html', {'form': form})



def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    for field in form.fields.values():
        field.widget.attrs.update({
            'class': 'form-control'
        })

    if form.is_valid():
        login(request, form.get_user())
        return redirect('home')

    return render(request, 'store/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


# --------------------
# CART
# --------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')



@login_required
def update_cart_qty(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1

    item.save()
    return JsonResponse({'status': 'ok'})


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if request.method == "POST":
        # ✅ CREATE ORDER (NO PAYMENT)
        Order.objects.create(
            user=request.user,
            total_price=total_price,
            status="Pending"
        )

        # Clear cart
        cart_items.delete()

        return render(request, 'store/order_success.html')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

#@login_required
#def order_history(request):
 #   orders = Order.objects.filter(user=request.user).order_by('-created_at')
  #  return render(request, 'store/orders.html', {'orders': orders})

@login_required
def order_success(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    Order.objects.create(user=request.user, total_price=total)
    cart_items.delete()

    return render(request, 'store/order_success.html')

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})

