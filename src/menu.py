from flask import Blueprint, jsonify, render_template, request

menu_bp = Blueprint('menu', __name__)

MENU_ITEMS = [
    {"id": "1", "name": "Margherita Pizza", "price": 11.99, "category": "Main", "ingredients": ["Tomato", "Mozzarella", "Basil"], "available": True},
    {"id": "2", "name": "Cheeseburger", "price": 9.99, "category": "Main", "ingredients": ["Beef Patty", "Cheddar", "Lettuce", "Tomato"], "available": True},
    {"id": "3", "name": "Caesar Salad", "price": 7.99, "category": "Main", "ingredients": ["Romaine", "Parmesan", "Croutons", "Caesar Dressing"], "available": False},
    {"id": "4", "name": "French Fries", "price": 3.99, "category": "Side", "ingredients": ["Potatoes", "Salt", "Oil"], "available": True},
    {"id": "5", "name": "Onion Rings", "price": 4.99, "category": "Side", "ingredients": ["Onions", "Batter", "Oil"], "available": True},
    {"id": "6", "name": "Coleslaw", "price": 2.99, "category": "Side", "ingredients": ["Cabbage", "Carrots", "Mayonnaise"], "available": False},
    {"id": "7", "name": "Chocolate Cake", "price": 5.99, "category": "Dessert", "ingredients": ["Chocolate", "Flour", "Sugar", "Eggs"], "available": True},
    {"id": "8", "name": "Ice Cream", "price": 3.99, "category": "Dessert", "ingredients": ["Cream", "Sugar", "Vanilla"], "available": True},
    {"id": "9", "name": "Soda", "price": 1.99, "category": "Drink", "ingredients": ["Carbonated Water", "Sugar", "Flavoring"], "available": True},
    {"id": "10", "name": "Orange Juice", "price": 2.99, "category": "Drink", "ingredients": ["Oranges"], "available": False},
]


@menu_bp.route('/menu', methods=['GET'])
def menu_page():
    categories = sorted(set(item['category'] for item in MENU_ITEMS))
    return render_template('menu.html', items=MENU_ITEMS, categories=categories)


@menu_bp.route('/api/menu', methods=['GET'])
def get_menu():
    category = request.args.get('category')
    items = MENU_ITEMS
    if category:
        items = [item for item in items if item['category'] == category]
    return jsonify({'items': items})
