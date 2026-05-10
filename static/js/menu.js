document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const clearBtn = document.getElementById('clear-filter');
    const itemsContainer = document.getElementById('menu-items');

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
                        <h3>${item.name}</h3>
                        <p class="price">$${item.price.toFixed(2)}</p>
                        <p class="ingredients"><strong>Ingredients:</strong> ${item.ingredients.join(', ')}</p>
                        ${item.available ? '' : '<span class="badge unavailable-badge">Not Available</span>'}
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
});
