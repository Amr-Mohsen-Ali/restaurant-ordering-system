from flask import Blueprint, jsonify, render_template, request

menu_bp = Blueprint('menu', __name__)

MENU_ITEMS = [
    {"id": "1", "name": "Pizza", "price": 240.0, "category": "Main", "ingredients": ["Tomato", "Mozzarella", "Basil"], "available": True, "image": "https://plus.unsplash.com/premium_photo-1733306588881-0411931d4fed?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "2", "name": "Classic Burger", "price": 185.0, "category": "Main", "ingredients": ["Beef Patty", "Cheddar", "Lettuce", "Tomato"], "available": True, "image": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?q=80&w=1115&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "3", "name": "Salad", "price": 95.0, "category": "Main", "ingredients": ["Romaine", "Parmesan", "Croutons", "Caesar Dressing"], "available": False, "image": "https://images.unsplash.com/photo-1607532941433-304659e8198a?q=80&w=1078&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "4", "name": "Fries", "price": 70.0, "category": "Side", "ingredients": ["Potatoes", "Salt", "Oil"], "available": True, "image": "https://images.unsplash.com/photo-1630384060421-cb20d0e0649d?q=80&w=1025&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "5", "name": "Onion Rings", "price": 85.0, "category": "Side", "ingredients": ["Onions", "Batter", "Oil"], "available": True, "image": "https://images.unsplash.com/photo-1639024471283-03518883512d?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "6", "name": "Coleslaw", "price": 55.0, "category": "Side", "ingredients": ["Cabbage", "Carrots", "Mayonnaise"], "available": False, "image": "https://images.unsplash.com/photo-1654458804670-2f4f26ab3154?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "7", "name": "Chocolate Cake", "price": 110.0, "category": "Dessert", "ingredients": ["Chocolate", "Flour", "Sugar", "Eggs"], "available": True, "image": "https://images.unsplash.com/photo-1517427294546-5aa121f68e8a?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "8", "name": "Ice Cream", "price": 80.0, "category": "Dessert", "ingredients": ["Cream", "Sugar", "Vanilla"], "available": True, "image": "https://images.unsplash.com/photo-1560008581-09826d1de69e?q=80&w=744&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "9", "name": "Soda", "price": 45.0, "category": "Drink", "ingredients": ["Carbonated Water", "Sugar", "Flavoring"], "available": True, "image": "https://plus.unsplash.com/premium_photo-1725075086631-b21a5642918b?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
    {"id": "10", "name": "Orange Juice", "price": 65.0, "category": "Drink", "ingredients": ["Oranges"], "available": False, "image": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
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
