async function updateQuantity(itemId, change) {
    try {
        const response = await fetch(`/cart/update/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ change: change })
        });
        
        const data = await response.json();
        if (response.ok) {
            const cartItem = document.querySelector(`[data-item-id="${itemId}"]`);
            if (data.quantity === 0) {
                cartItem.remove();
            } else {
                cartItem.querySelector('.quantity').textContent = data.quantity;
            }
            document.querySelector('.subtotal-amount').textContent = data.subtotal;
            
            // Update cart count in navbar
            const cartCount = document.querySelector('.cart-count');
            if (cartCount) {
                cartCount.textContent = `(${data.cart_count})`;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function removeItem(itemId) {
    try {
        const response = await fetch(`/cart/remove/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        if (response.ok) {
            const cartItem = document.querySelector(`[data-item-id="${itemId}"]`);
            cartItem.remove();
            document.querySelector('.subtotal-amount').textContent = data.subtotal;
            
            // If cart is empty after removal, refresh the page
            const remainingItems = document.querySelectorAll('.cart-item');
            if (remainingItems.length === 0) {
                location.reload();
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function placeOrder(event) {
    event.preventDefault(); // Prevent form from submitting normally
    
    try {
        const response = await fetch('/place-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            alert('Order placed successfully!'); // Add feedback
            window.location.href = '/orders';
        } else {
            const data = await response.json();
            alert('Error placing order: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error placing order. Please try again.');
    }
}

function showLoginMessage(event) {
    event.preventDefault();
    alert('Please log in to view your cart');
}