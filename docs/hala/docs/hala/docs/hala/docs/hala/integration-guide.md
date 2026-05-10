# Integration Guide — Cart Feature

## For the Menu feature

When the customer clicks "Add to Cart" on any menu item, call this:

```python
from cart import Cart

cart = Cart()

result = cart.add_to_cart(
    item_id    = item["item_id"],
    unit_price = item["unit_price"],
    quantity   = 1
)

if result["success"]:
    print(f"Cart total is now EGP {result['cart_total']}")
```

Your menu item dict must have at least these two keys:

```python
item = {
    "item_id":    "item_001",
    "unit_price": 75.00
}
```

---

## For the Order Placement feature

When the customer clicks "Place Order", call this function
and pass the result to your place_order() method:

```python
def get_checkout_payload(cart: Cart) -> dict:
    return {
        "items": [
            {
                "item_id":    item_id,
                "quantity":   data["quantity"],
                "unit_price": data["unit_price"],
                "line_total": round(data["unit_price"] * data["quantity"], 2)
            }
            for item_id, data in cart.items.items()
        ],
        "cart_total":      cart.cart_total,
        "cart_item_count": cart.cart_item_count
    }

# Call it like this:
# order_result = place_order(get_checkout_payload(cart))
```

---

## File to import

`cart.py` is in the project root. Import it with:

```python
from cart import Cart
```

---

## Important — agree on item IDs before merging

I use string IDs in the format `"item_001"`, `"item_002"` and so on.
The Menu feature must use the same IDs, otherwise the cart will not
find the items. Please confirm your ID format before we combine branches.
