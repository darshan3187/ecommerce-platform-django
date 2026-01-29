document.addEventListener('DOMContentLoaded', function () {
    const detailsTab = document.getElementById('details-tab');
    const shippingTab = document.getElementById('shipping-tab');
    const detailsContent = document.getElementById('details-content');
    const shippingContent = document.getElementById('shipping-content');

    console.log("product_detail.js loaded");

    const toggleBtn = document.getElementById("toggleReviewForm");
    const formWrapper = document.getElementById("reviewFormWrapper");

    if (!toggleBtn || !formWrapper) {
        console.error("Review toggle elements not found");
        return;
    }

    toggleBtn.addEventListener("click", function () {
        formWrapper.classList.toggle("hidden");
        formWrapper.scrollIntoView({
            behavior: "smooth",
            block: "center",
        });
    });


    shippingTab.addEventListener('click', function () {
        detailsContent.classList.add('hidden');
        shippingContent.classList.remove('hidden');

        detailsTab.classList.remove('text-indigo-600', 'border-indigo-600');
        detailsTab.classList.add('text-gray-600');

        shippingTab.classList.remove('text-gray-600');
        shippingTab.classList.add('text-indigo-600', 'border-b-2', 'border-indigo-600');
    });

    detailsTab.addEventListener('click', function () {
        shippingContent.classList.add('hidden');
        detailsContent.classList.remove('hidden');

        shippingTab.classList.remove('text-indigo-600', 'border-indigo-600');
        shippingTab.classList.add('text-gray-600');

        detailsTab.classList.remove('text-gray-600');
        detailsTab.classList.add('text-indigo-600', 'border-b-2', 'border-indigo-600');
    });

    // Quantity Selector Functionality
    const decreaseBtn = document.getElementById('decreaseBtn');
    const increaseBtn = document.getElementById('increaseBtn');
    const quantityInput = document.getElementById('quantityInput');
    const quantityField = document.getElementById('quantityField');

    if (decreaseBtn && increaseBtn && quantityInput) {
        decreaseBtn.addEventListener('click', function (e) {
            e.preventDefault();
            let currentValue = parseInt(quantityInput.value) || 1;
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
                quantityField.value = quantityInput.value;
            }
        });

        increaseBtn.addEventListener('click', function (e) {
            e.preventDefault();
            let currentValue = parseInt(quantityInput.value) || 1;
            let maxValue = parseInt(quantityInput.max) || 100;
            if (currentValue < maxValue) { quantityInput.value = currentValue + 1; quantityField.value = quantityInput.value; }
        }); 
        //Allow manual input changes 
        quantityInput.addEventListener('change', function () {
            let value = parseInt(this.value) ||
                1; let max = parseInt(this.max) || 100; let min = parseInt(this.min) || 1; if (value < min) this.value = min; if (value >
                    max) this.value = max;
            quantityField.value = this.value;
        });
    }

    // Handle add to cart form submission
    const addToCartForm = document.getElementById('addToCartForm');
    if (addToCartForm) {
        addToCartForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const quantity = document.getElementById('quantityInput').value;
            formData.set('quantity', quantity);

            const button = document.getElementById('addToCart_btn');
            const originalText = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<span>Adding...</span>';

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        showNotification('Item added to cart', 'success');
                        // Update cart count
                        const cartCount = document.getElementById('cart-count');
                        if (cartCount) {
                            cartCount.textContent = data.cart_item_count;
                        }
                    } else {
                        showNotification(data.message || 'Failed to add item to cart', 'error');
                    
                        // Reset quantity
                        if (quantityInput) {
                            quantityInput.value = 1;
                            quantityField.value = 1;
                        }
                    }
                })
                .catch(error => {
                    showNotification('Error adding item to cart', 'error');
                    console.error('Error:', error);
                })
                .finally(() => {
                    button.disabled = false;
                    button.innerHTML = originalText;
                });
        });
    }
});

// Show notification helper
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-4 py-3 rounded-lg text-white font-semibold z-50 ${type === 'success' ? 'bg-green-500' : 'bg-red-500'
        }`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

