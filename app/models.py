from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association table for Product-Category many-to-many relationship
product_categories = db.Table('product_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

# Remove primary_key=True from order_id and product_id
order_products = db.Table('order_products',
    db.Column('id', db.Integer, primary_key=True),  # Add this new primary key
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('quantity', db.Integer, default=1),
    db.Column('price_at_time', db.Float)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(500))
    
    # Relationships
    categories = db.relationship('Category', secondary=product_categories, backref=db.backref('products', lazy=True))
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)
    
    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)

    def __repr__(self):
        return f"Product('{self.name}', ${self.price})"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f"Category('{self.name}')"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"CartItem(Product: '{self.product.name}', Quantity: {self.quantity})"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='PENDING')
    shipping_address = db.Column(db.Text, nullable=False)
    tracking_number = db.Column(db.String(100))
    
    products = db.relationship('Product', secondary=order_products, backref=db.backref('orders', lazy=True))

    def get_products_with_quantities(self):
        result = db.session.query(
            Product,
            order_products.c.quantity,
            order_products.c.price_at_time
        ).join(
            order_products,
            and_(
                order_products.c.product_id == Product.id,
                order_products.c.order_id == self.id
            )
        ).all()
        return result

    def __repr__(self):
        return f"Order('{self.id}', Status: '{self.status}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Review(Product: '{self.product.name}', Rating: {self.rating})"