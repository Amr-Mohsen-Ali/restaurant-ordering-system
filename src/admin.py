from datetime import date
from flask import Blueprint, render_template, request, redirect, flash, jsonify
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from src.database import db, MenuItem, Order, User, Reservation, WaiterCall
from src.auth import require_role
from src.constants import ROLE_ADMIN, ORDER_STATUS_DELIVERED

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
waiter_api_bp = Blueprint('waiter_api', __name__, url_prefix='/api')


@admin_bp.route('/menu/add', methods=['POST'])
@require_role(ROLE_ADMIN)
def add_menu_item():
    name = request.form.get('name')
    category = request.form.get('category')
    price = request.form.get('price', type=float)
    image = request.form.get('image')
    ingredients_raw = request.form.get('ingredients', '')
    available = request.form.get('available') == 'on'
    
    ingredients = [i.strip() for i in ingredients_raw.split(',') if i.strip()]
    
    item = MenuItem(
        name=name, 
        category=category, 
        price=price, 
        image=image, 
        ingredients=ingredients, 
        available=available
    )
    db.session.add(item)
    db.session.commit()
    flash('Menu item added successfully.', 'success')
    return redirect('/admin/dashboard')

@admin_bp.route('/menu/delete/<int:item_id>', methods=['POST'])
@require_role(ROLE_ADMIN)
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item deleted.', 'success')
    return redirect('/admin/dashboard')

@admin_bp.route('/menu/toggle/<int:item_id>', methods=['POST'])
@require_role(ROLE_ADMIN)
def toggle_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.available = not item.available
    db.session.commit()
    status_str = "Available" if item.available else "Unavailable"
    flash(f'Menu item "{item.name}" is now {status_str}.', 'success')
    return redirect('/admin/dashboard')

@admin_bp.route('/staff/add', methods=['POST'])
@require_role(ROLE_ADMIN)
def add_staff():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists.', 'error')
    else:
        user = User(
            username=username, 
            password_hash=generate_password_hash(password), 
            role='staff'
        )
        db.session.add(user)
        db.session.commit()
        flash('Staff added successfully.', 'success')
        
    return redirect('/admin/dashboard')

@admin_bp.route('/waiter-calls/resolve/<int:call_id>', methods=['POST'])
@require_role('admin', 'staff')  # both admin and staff can resolve
def resolve_waiter_call(call_id):
    call = WaiterCall.query.get_or_404(call_id)
    call.status = 'resolved'
    db.session.commit()
    return redirect(request.referrer or '/staff')

@waiter_api_bp.route('/call-waiter', methods=['POST'])
def call_waiter():
    data = request.get_json() or {}
    table_number = data.get('table_number')
    if not table_number:
        return jsonify({'success': False, 'error': 'Table number required'}), 400
    
    # Check if there is an existing pending call for this table
    existing = WaiterCall.query.filter_by(table_number=str(table_number), status='pending').first()
    if not existing:
        new_call = WaiterCall(table_number=str(table_number), status='pending')
        db.session.add(new_call)
        db.session.commit()
        
    return jsonify({'success': True})

@waiter_api_bp.route('/waiter-calls', methods=['GET'])
def get_waiter_calls():
    calls = WaiterCall.query.filter_by(status='pending').order_by(WaiterCall.created_at.desc()).all()
    return jsonify({
        'success': True,
        'calls': [c.to_dict() for c in calls]
    })
