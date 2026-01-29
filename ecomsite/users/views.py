from django.shortcuts import render , redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from shop.models import Cart, CartItem

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)  # Pass request.POST here
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, Your Account is Created Successfully!')
            return redirect('users:login')
    else:  # Add this else!
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:register')

@login_required
def profile(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = []
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
    
    context = {
        'cart_items': cart_items
    }
    return render(request, 'users/profile.html', context)
