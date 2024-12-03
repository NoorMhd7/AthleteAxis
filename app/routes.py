from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from .forms import RegistrationForm, LoginForm
from .models import Product, Category, CartItem
import json
from pathlib import Path

main = Blueprint('main', __name__)

# Index Route (Home Page)
@main.route('/')
def index():
    print("Reached index route")
    return render_template('base.html')

# About Page Route
@main.route('/about')
def about():
    return 'About Page'

# Contact Page Route
@main.route('/contact')
def contact():
    return 'Contact Page'

# Cart Page Route
@main.route('/cart')
def cart():
    return 'Cart Page'


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Change the hashing method to 'pbkdf2:sha256'
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            print(f"Error: {e}")  # For debugging
            
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
@login_required  # This ensures only logged-in users can access this route
def logout():
    logout_user()  # This comes from flask-login
    flash('You have been logged out successfully.', 'success')  # Add a success message
    return redirect(url_for('main.index'))

@main.route('/shop')
def shop():
    try:
        products = Product.query.all()
        print(f"Number of products found: {len(products)}")  # Debug print
        for product in products:
            print(f"Product: {product.name}, Price: ${product.price}")  # Debug print
        return render_template('shop.html', products=products)
    except Exception as e:
        print(f"Error in shop route: {str(e)}")  # Debug print
        return f"Error: {str(e)}"

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@main.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id, 
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Item added to cart successfully!', 'success')
    return redirect(url_for('main.shop'))

@main.route('/initialize-db')
def initialize_db():
    try:
        product = Product(
            name='Professional Running Shoes',
            description='High-performance running shoes designed for athletes',
            price=159.99,
            quantity=50,
            image='/static/images/running-shoes.jpg'
        )
        
        db.session.add(product)
        db.session.commit()
        
        added_product = Product.query.first()
        if added_product:
            return f"""
                Product successfully added:<br>
                Name: {added_product.name}<br>
                Price: ${added_product.price}<br>
                <a href='/shop'>View Shop</a> | 
                <a href='/manage-products'>Add More Products</a>
            """
        return "Product was not added successfully."
        
    except Exception as e:
        db.session.rollback()
        return f"Database error: {str(e)}"
    
@main.route('/setup-store')
def setup_store():
    try:
        # Check for existing products
        existing_products = Product.query.all()
        
        if existing_products:
            return redirect(url_for('main.shop'))

        # Load products from JSON file
        json_path = Path(__file__).parent / 'products.json'
        
        with open(json_path, 'r') as file:
            data = json.load(file)
            
        # Create new products from JSON data
        for product_data in data['products']:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity'],
                image=product_data['image']
            )
            db.session.add(product)

        db.session.commit()
        return redirect(url_for('main.shop'))

    except Exception as e:
        db.session.rollback()
        return f"Error setting up store: {str(e)}"
    
@main.route('/cleanup-products')
def cleanup_products():
    try:
        Product.query.delete()
        db.session.commit()
        return "All products removed. Visit /setup-store to reinitialize the store."
    except Exception as e:
        db.session.rollback()
        return f"Error cleaning up products: {str(e)}"