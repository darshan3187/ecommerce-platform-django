from decimal import Decimal
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from urllib3 import request
from .models import Cart, ProductInfo, CartItem , Order , OrderItem , Review
from .form import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Random
from django.views.decorators.cache import cache_page
import random
from django.db import transaction
from .form import ReviewForm


def home(request):
    # Get 4 random trending products
    trending_products = ProductInfo.objects.order_by( Random() )[:4]
    featured_products = ProductInfo.objects.order_by('-price')[:4]

    # Get 5 random categories
    all_categories = list(ProductInfo.objects.values_list('category', flat=True).distinct())
    random.shuffle(all_categories)  # shuffle the list
    categories = all_categories[:5]  # pick first 5


    # Prepare 4 products per category
    categories_with_products = []
    for category in categories:
        products = ProductInfo.objects.filter(category=category).order_by(Random())[:4]  # first 4 products
        categories_with_products.append((category, products))

    context = {
        'trending_products': trending_products,
        'featured_products': featured_products,
        'categories': categories,
        'categories_with_products': categories_with_products,
    }
    return render(request, 'shop/home.html', context)


# @cache_page(60 * 10)
def category_view(request):
    categories = (
        ProductInfo.objects
        .order_by('category')
        .values_list('category', flat=True)
        .distinct()

    )

    paginator = Paginator(categories, 6)
    page_number = request.GET.get('page')
    page_categories = paginator.get_page(page_number)

    categories_with_products = []
    for category in page_categories:
        products = (
            ProductInfo.objects
            .filter(category=category)
            .only('title', 'image')
            .order_by('-id')[:4]
        )
        categories_with_products.append((category, products))

    return render(
        request,
        "shop/category_list.html",
        {
            "categories_with_products": categories_with_products,
            "page_obj": page_categories
        }
    )


def product_list(request):
    products = ProductInfo.objects.all()

    # Search filter
    product_name = request.GET.get('product_name')
    if product_name:
        products = products.filter(title__icontains=product_name)

    # Category filter
    category = request.GET.get('category')
    if category and category != 'all':
        products = products.filter(category__iexact=category)

    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-id')

    # Get all unique categories for the filter dropdown
    categories = ProductInfo.objects.values_list('category', flat=True).distinct()

    # Get min and max prices for range
    all_products = ProductInfo.objects.all()
    min_price_available = all_products.order_by('price').first().price if all_products.exists() else 0
    max_price_available = all_products.order_by('-price').first().price if all_products.exists() else 1000

    # Paginate with 16 products per page
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'min_price_available': min_price_available,
        'max_price_available': max_price_available,
        'selected_category': category,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
    }

    return render(request, "shop/product_list.html", context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(ProductInfo, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            product=product,
            user=request.user
        ).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        if user_review:
            return redirect(request.path)  # prevent duplicates

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect(request.path)
    else:
        form = ReviewForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    })


@require_POST
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(ProductInfo, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid quantity'}, status=400)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    from django.db.models import Sum
    total_items = CartItem.objects.filter(cart=cart).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return JsonResponse({
        'status': 'success',
        'message': 'Item added to cart',
        'cart_count': total_items
    })



@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')

    cart_total = sum(item.subtotal for item in cart_items)
    tax = cart_total * Decimal(0.1)
    total = cart_total + tax

    return render(request, "shop/cart.html", {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax': tax,
        'total': total,
    })



@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == "POST":
        item.delete()
        return redirect('shop:cart')

    return render(request, 'shop/cart_remove.html', {'item': item})


@require_POST
@login_required
def update_cart_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        return JsonResponse({'status': 'success'})
    except ValueError:
        return JsonResponse({'status': 'error'}, status=400)



@login_required
def checkout(request):
    if not request.session.session_key:
        request.session.create()
    
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')

    if not cart_items.exists():
        return redirect('shop:product_list')

    form = CheckoutForm(request.POST or None)

    cart_total = sum(item.subtotal for item in cart_items)
    tax = cart_total * Decimal(0.1)
    total = cart_total + tax

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart_items.delete() # clear cart
            return redirect('shop:product_list')  # replace with thank-you page later
        
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax': tax,
        'total': total,
        'Form': form,
    }

    return render(request, "shop/checkout.html", context)

