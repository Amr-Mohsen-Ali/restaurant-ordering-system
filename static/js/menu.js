document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const clearBtn = document.getElementById('clear-filter');
    const itemsContainer = document.getElementById('menu-items');
    const cartMessage = document.getElementById('cart-message');

    function escapeHtml(value) {
        return String(value).replace(/[&<>"']/g, (char) => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[char]));
    }

function renderCartActions(item) {
        const disabled = item.available ? '' : 'disabled';
        return `
            <div class="menu-cart-actions">
                <label for="quantity-${escapeHtml(item.id)}">Qty</label>
                <input
                    id="quantity-${escapeHtml(item.id)}"
                    class="cart-quantity"
                    type="number"
                    min="1"
                    max="20"
                    value="1"
                    ${disabled}
                >
                <button
                    class="add-to-cart-btn"
                    data-item-id="${escapeHtml(item.id)}"
                    data-item-name="${escapeHtml(item.name)}"
                    data-price="${Number(item.price)}"
                    ${disabled}
                >
                    Add to Cart
                </button>
            </div>
        `;
    }

    function showCartMessage(message, isError = false) {
        cartMessage.hidden = false;
        cartMessage.classList.toggle('error', isError);
        cartMessage.innerHTML = isError
            ? escapeHtml(message)
            : `${escapeHtml(message)} <a href="/cart">Go to Cart</a>`;
    }

    function fetchItems(category) {
        const url = category ? `/api/menu?category=${encodeURIComponent(category)}` : '/api/menu';
        fetch(url)
            .then(res => res.json())
            .then(data => {
                itemsContainer.innerHTML = '';
                data.items.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'menu-item' + (item.available ? '' : ' unavailable');
                    div.innerHTML = `
                        <img src="${item.image}" alt="${escapeHtml(item.name)}">
                        <h3>${escapeHtml(item.name)}</h3>
                        <p class="price">${item.price.toFixed(2)}</p>
                        <p class="ingredients"><strong>Ingredients:</strong> ${item.ingredients.map(escapeHtml).join(', ')}</p>
                        ${item.available ? '' : '<span class="badge unavailable-badge">Not Available</span>'}
                        ${renderCartActions(item)}
                    `;
                    itemsContainer.appendChild(div);
                });
                updateFilterState(category);
            });
    }

    function updateFilterState(activeCategory) {
        filterBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === (activeCategory || ''));
        });
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            fetchItems(btn.dataset.category);
        });
    });

    clearBtn.addEventListener('click', () => {
        fetchItems('');
    });

    itemsContainer.addEventListener('click', async (event) => {
        const button = event.target.closest('.add-to-cart-btn');
        if (!button || button.disabled) {
            return;
        }

        const menuItem = button.closest('.menu-item');
        const quantityInput = menuItem.querySelector('.cart-quantity');
        const quantity = Number(quantityInput.value);

        if (!Number.isInteger(quantity) || quantity < 1 || quantity > 20) {
            showCartMessage('Quantity must be between 1 and 20.', true);
            quantityInput.focus();
            return;
        }

        button.disabled = true;

        try {
const response = await fetch('/cart/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    item_id: button.dataset.itemId,
                    item_name: button.dataset.itemName,
                    price: Number(button.dataset.price),
                    quantity
                })
            });
            const data = await response.json();

            if (!response.ok || !data.success) {
                showCartMessage(data.error || 'Could not add item to cart.', true);
                return;
            }

            showCartMessage('Added to cart!');
            if (typeof window.updateCartBadge === 'function') {
                window.updateCartBadge();
            }
        } catch (error) {
            showCartMessage('Could not add item to cart.', true);
        } finally {
            button.disabled = false;
        }
    });
});
