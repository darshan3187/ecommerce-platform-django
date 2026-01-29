import requests
from .models import ProductInfo
from django.conf import settings

def fetch_products():
    url = settings.DUMMY_PRODUCTS_API # Use the setting from settings.py
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception("Failed to fetch products")

    products = res.json()["products"]

    for item in products:
        discount_price = item["price"] - (
            item["price"] * item["discountPercentage"] / 100
        )

        # Get first image from images array with proper error handling
        image_url = ""
        if "images" in item and isinstance(item["images"], list) and len(item["images"]) > 0:
            image_url = item["images"][0]
        elif "thumbnail" in item:
            image_url = item["thumbnail"]
        
        ProductInfo.objects.update_or_create(
            api_id=item["id"],
            defaults={
                "title": item["title"],
                "price": item["price"],
                "discount_price": round(discount_price, 2),
                "category": item["category"],
                "description": item["description"],
                "image": image_url,
                "warranty_information": item["warrantyInformation"],
                "shipping_info": item["shippingInformation"],
                'availability': item["availabilityStatus"],
                'stock': item["stock"],
            }
        )
