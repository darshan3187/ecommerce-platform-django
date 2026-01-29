from django.conf import settings
from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

class ProductInfo(models.Model):
    api_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=150)
    description = models.TextField()
    image = models.URLField(max_length=500)
    warranty_information = models.CharField(max_length=200)
    shipping_info = models.CharField(max_length=200)
    availability = models.CharField(max_length=50, default="In Stock")
    stock = models.IntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Product info"
        verbose_name_plural = "Product info"

    def __str__(self):
        return self.title

    @property
    def discount_percentage(self):
        if self.discount_price:
            return int((-(self.discount_price - self.price) / self.discount_price) * 100)
        return 0


class Review(models.Model):
    product = models.ForeignKey(
        ProductInfo,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1–5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # IMPORTANT

    def __str__(self):
        return f"{self.product} - {self.rating}"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Cart ({self.user.username})"
        return f"Cart (session {self.session_key})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['product', 'cart']

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def subtotal(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"Order By {self.order.full_name}"