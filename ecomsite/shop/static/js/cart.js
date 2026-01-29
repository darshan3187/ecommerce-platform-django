document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    function getCsrfToken() {
        return csrfToken;
    }

    function updateCartQuantity(itemId, quantity) {
        fetch(`/shop/update-cart/${itemId}/`, {
            method: 'POST',
            body: JSON.stringify({ quantity: quantity }),
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    location.reload();
                }
            })
            .catch(error => console.error('Error updating cart:', error));
    }

    // Quantity decrease
    document.querySelectorAll('.quantity-decrease').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const itemId = btn.getAttribute('data-item-id');
            const input = document.querySelector(`input[data-item-id="${itemId}"]`);
            const value = Math.max(1, parseInt(input.value) - 1);
            input.value = value;
            updateCartQuantity(itemId, value);
        });
    });

    // Quantity increase
    document.querySelectorAll('.quantity-increase').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const itemId = btn.getAttribute('data-item-id');
            const input = document.querySelector(`input[data-item-id="${itemId}"]`);
            const max = parseInt(input.max) || 100;
            const value = Math.min(max, parseInt(input.value) + 1);
            input.value = value;
            updateCartQuantity(itemId, value);
        });
    });

    // Quantity input change
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function () {
            let value = parseInt(this.value) || 1;
            const min = parseInt(this.min) || 1;
            const max = parseInt(this.max) || 100;

            value = Math.max(min, Math.min(max, value));
            this.value = value;

            const itemId = this.getAttribute('data-item-id');
            updateCartQuantity(itemId, value);
        });
    });
});
