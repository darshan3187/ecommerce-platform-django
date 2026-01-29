from django.urls import path
from shop import views

app_name='shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.category_view, name='category_list'),
    path('shop/', views.product_list, name='product_list'),
    path('detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart'),
    path('checkout/', views.checkout , name= 'checkout'),
]
