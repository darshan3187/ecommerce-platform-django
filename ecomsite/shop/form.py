from django import forms
from .models import Order
from .models import Review

from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]

        widgets = {
            "rating": forms.Select(
                choices=[(i, f"{i} ⭐") for i in range(1, 6)],
                attrs={
                    "class": (
                        "w-full sm:w-40 px-3 py-2 border border-gray-300 "
                        "rounded-lg bg-white text-gray-700 text-sm "
                        "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                        "focus:border-indigo-500 transition"
                    )
                },
            ),
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your honest review here…",
                    "class": (
                        "w-full px-3 py-2 border border-gray-300 rounded-lg "
                        "text-gray-700 text-sm resize-none "
                        "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                        "focus:border-indigo-500 transition"
                    ),
                }
            ),
        }


class CheckoutForm(forms.ModelForm):
    class Meta():
        model = Order  
        fields = ['full_name', 'email', 'address', 'city', 'postal_code', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update(
            {'class': 'w-full px-3 py-2 border rounded', 'placeholder': 'Full Name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'w-full px-3 py-2 border rounded', 'placeholder': 'Email Address'})
        self.fields['address'].widget.attrs.update(
            {'class': 'w-full px-3 py-2 border rounded', 'placeholder': 'Shipping Address'})
        self.fields['city'].widget.attrs.update(
            {'class': 'w-full px-3 py-2 border rounded', 'placeholder': 'City'})
        self.fields['postal_code'].widget.attrs.update(
            {'class': 'w-full px-3 py-2 border rounded', 'placeholder': 'Postal Code'})
        self.fields['country'].widget.attrs.update(
            {'class': 'w-full px-3 py-2 border rounded', 'placeholder': 'Country'})