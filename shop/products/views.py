import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.core.files.storage import FileSystemStorage
from shop.settings import BASE_DIR



from .models import Product, Category, Card, Cart
from .forms import CardCreationForm, ProductCreationForm, CategoryCreationForm



def list_products(request):
    products = Product.objects.all()
    
    ctx = {
        'title': 'Shop',
        'products': products
    }
    
    return render(request, 'list_products.html', ctx)


def product_details(request, id: int):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponseNotFound(('Product does not exist'))
    context = {
        'title': product.name,
        'product': product,
    }
    return render(request, 'product_details.html', context=context)



@login_required()
def add_to_cart(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    try:
        cart = Cart.objects.get(product=product, user=request.user, paid_status=Cart.PaidStatus.IN_CART)
        cart.quantity += 1
        cart.save()
    except Cart.DoesNotExist:
        Cart.objects.create(user=request.user, product=product)
    return redirect('list_products')


@login_required()
def my_cart(request):
    user_carts = Cart.objects.select_related('product').filter(user=request.user, paid_status=Cart.PaidStatus.IN_CART)
    total_cost = sum([cart.product.price * cart.quantity for cart in user_carts])    
    context = {
        'title': 'Cart',
        'user_carts' : user_carts,
        'total_cost': total_cost
    }
    
    return render(request, 'my_cart.html', context)


@login_required()
def delete_from_cart(request, product_id):
    try:
        cart = Cart.objects.get(user=request.user, product__id=product_id,  paid_status=Cart.PaidStatus.IN_CART)
        cart.quantity -= 1
        cart.save()
        if cart.quantity < 1:
            cart.delete()
        user_carts = Cart.objects.select_related('product').filter(user=request.user, paid_status=Cart.PaidStatus.IN_CART)
        total_cost = sum([cart.product.price * cart.quantity for cart in user_carts])    


    except Product.DoesNotExist:
        return HttpResponseNotFound(('Product is not in a cart'))
    context = {
        'title': 'Cart',
        'user_carts' : user_carts,
        'total_cost': total_cost

    }
    return render(request, 'my_cart.html', context=context)


@login_required()
def create_product(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        category = request.POST.get('categories')
        product_form = ProductCreationForm(request.POST)
        if product_form.is_valid():
            product_image = product_form.cleaned_data['name'].replace(" ", '_')
            
            static_dir = os.path.join(BASE_DIR, 'products/static/')

            upload = request.FILES['image']
            FileSystemStorage().save(f'{static_dir}/{product_image}.jpg', upload)

            product = product_form.save(commit=False)
            product.image_url = product_image + '.jpg'
            try:
                category_obj = Category.objects.get(name=category)
            except Category.DoesNotExist:
                category_obj = Category.objects.create(name=category)
            product.category = category_obj
            product.save()


            return redirect('product_details', product.id)

    else:
        product_form = ProductCreationForm()
    categories = Category.objects.all()

    context = {
        'product_form': product_form,
        'categories': categories
        
    }
    return render(request, 'create_product.html', context)


@login_required()
def create_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category')
        try:
            Category.objects.get(name=category_name)
        except Category.DoesNotExist:
             Category.objects.create(name=category_name)
             
    return redirect('create_product')


@login_required()
def delete_product(request, product_id):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        fss = FileSystemStorage()
        static_dir = os.path.join(BASE_DIR, 'products/static')
        fss.delete(f'{static_dir}/{product.image_url}')
        return redirect('list_products')
    else:
        return HttpResponseForbidden()


@login_required()
def add_card(request):
    if request.method == 'POST':
        card_form = CardCreationForm(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            card.user = request.user      
            card.save()
            return redirect('my_cards')
    else:
        card_form = CardCreationForm()
        
    context = {
        'form': card_form
    }
    return render(request, 'add_card.html', context)

@login_required()
def my_cards(request):
    user_cards = Card.objects.filter(user=request.user)
    return render(request, 'my_cards.html', {'cards': user_cards, 'pay_button': False})

@login_required()
def delete_card(request, card_id):
    card = Card.objects.filter(pk=card_id)
    card.delete()
    user_cards = Card.objects.all()
    return render(request, 'my_cards.html', {'cards': user_cards})


@login_required()
def select_card_for_payment(request):
    user_cards = Card.objects.filter(user=request.user)
    return render(request, 'my_cards.html', {'cards': user_cards, 'pay_button': True})


@login_required()
def payment(request, card_id):
    user_carts = Cart.objects.select_related('product').filter(user=request.user)
    for cart in user_carts:
        cart.paid_status = Cart.PaidStatus.PAID
        cart.product.quantity -= cart.quantity
        cart.product.save()
        cart.save()
    # total_cost = sum([cart.product.price * cart.quantity for cart in user_carts])
    
    return redirect('list_purchases')
    
    
@login_required()
def list_purchases(request):
    purchases = Cart.objects.select_related('product').filter(user=request.user, paid_status=Cart.PaidStatus.PAID)
    context = {
        'title': 'Purchases',
        'purchases' : purchases,
    }
    
    return render(request, 'list_purchases.html', context)
