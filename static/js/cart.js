// static/js/cart.js

async function addToCart(itemId, price) {
    const response = await fetch('/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: itemId, price: price, quantity: 1 })
    });
    
    const data = await response.json();
    
    if (data.success) {
        document.querySelector('[data-testid="cart-empty-message"]').style.display = 'none';
        document.getElementById('cart-items').style.display = 'block';
        document.querySelector('[data-testid="cart-total"]').innerText = data.total.toFixed(2);
        document.querySelector('[data-testid="cart-badge"]').innerText = "1"; 
        document.querySelector('[data-testid="cart-error-message"]').style.display = 'none';
    } else {
        const errorEl = document.querySelector('[data-testid="cart-error-message"]');
        errorEl.innerText = data.error || "Failed to add item";
        errorEl.style.display = 'block';
    }
}
