from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """The database model for the User table.
    This is used to store the login information for users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    """Allow users to be loaded from a database"""
    return User.query.get(int(id))


customerDelivery = db.Table('customerDelivery',
                             db.Column('Delivery', db.Integer, db.ForeignKey('delivery.id', ondelete="CASCADE",
                                                                             onupdate="CASCADE"), primary_key=True),
                             db.Column('Customer', db.Integer, db.ForeignKey('customer.id', onupdate="CASCADE",
                                                                             ondelete="CASCADE"), primary_key=True),
                             db.Column('Order Date', db.DateTime),
                             db.Column('Expected Delivery Date', db.DateTime, nullable=False))


class Customer(db.Model):
    """
        The database model for the Customer table.
        This is used to store the information about a Customer.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column("First Name", db.String(64), index=True, nullable=False)
    last_name = db.Column("Last Name", db.String(64), index=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True)
    address = db.Column("Address", db.String(128))
    phone_number = db.Column("Phone Number", db.VARCHAR(12), unique=True, nullable=False)
    pallets = db.relationship('Pallet', backref='customer', lazy=True)


class Delivery(db.Model):
    """
        The Database model for the Delivery Table.
        Used to store information about the Delivery destination of the Pan
    """
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column('Address', db.String(128), index=True, nullable=False)
    pan_id = db.Column('Pan ID', db.Integer, db.ForeignKey('pan.id', onupdate='Cascade', ondelete='SET NULL'),
                       nullable=True)
    pallet = db.relationship('Pallet', backref='Delivery', lazy=True)
    customerDelivery = db.relationship('Customer', secondary=customerDelivery, lazy='select',
                                       backref=db.backref('deliveries', lazy=True))
    panCoord = db.relationship('PanCoordinator', backref='Delivery', lazy=True)


class Content(db.Model):
    """
        #The database model for the Content table
        #This is used to store the information on the contents
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    expiry_date = db.Column(db.Date, index=True)


palletContent = db.Table('palletContent',
                          db.Column("pallet_id", db.Integer, db.ForeignKey('pallet.id', ondelete="CASCADE",
                                                                           onupdate="CASCADE"), primary_key=True),
                          db.Column("content_id", db.Integer, db.ForeignKey('content.id', ondelete="CASCADE",
                                    onupdate="CASCADE"), primary_key=True),
                          db.Column("content_type", db.String(64), index=True),
                          db.Column("quantity", db.Integer, db.CheckConstraint('quantity > 0')))


class Pallet(db.Model):
    """
        The database model for the Pallet table.
        This is used to store the information about a pallet
    """
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column('Weight', db.Numeric, db.CheckConstraint('Weight > 0.0'), nullable=False)
    height = db.Column('Height', db.Numeric, db.CheckConstraint('Height > 0.0'), nullable=False)
    category = db.Column('Category', db.String(1), nullable=False)
    stack_able = db.Column('Can Stack', db.Boolean, nullable=False)
    customer_id = db.Column('Customer ID', db.Integer, db.ForeignKey('customer.id', ondelete="CASCADE",
                                                                     onupdate="CASCADE"), nullable=False)
    delivery_id = db.Column('Delivery ID', db.Integer, db.ForeignKey('delivery.id', ondelete='CASCADE',
                                                                     onupdate='CASCADE'), nullable=False)
    contents = db.relationship('Content', secondary=palletContent, lazy='select',
                               backref=db.backref('pallets', lazy=True))
    pan_coord = db.relationship('PanCoordinator', backref='pallet', lazy=True)
    db.CheckConstraint(db.Column('Category') is 'F' or db.Column('Category') is 'f' or db.Column('Category') is 'C'
                       or db.Column('Category') is 'c' or db.Column('Category') is 'D' or db.Column('Category') is 'd')


class Pan(db.Model):
    """
        #The database model for the Pan table.
        #This is used to store the information about a pan
    """
    id = db.Column('id', db.Integer, primary_key=True)
    weight = db.Column('Weight', db.Numeric, db.CheckConstraint('Weight > 0.0'), nullable=False)
    height = db.Column('Height', db.Numeric, db.CheckConstraint('Height > 0.0'), nullable=False)
    width = db.Column('Width', db.Numeric, db.CheckConstraint('Width > 0.0'), nullable=False)
    length = db.Column('Length', db.Numeric, db.CheckConstraint('Length > 0.0'), nullable=False)
    rail_height = db.Column('Rail Height', db.Numeric, db.CheckConstraint('Rail Height > 0.0 and Rail Height < Height'))
    cost = db.Column('Cost', db.Numeric, db.CheckConstraint('Cost >= 0'))
    delivery = db.relationship('Delivery', backref='pan', lazy=True)


class PanCoordinator(db.Model):
    """
        A mode that allow the Storing storing of pallet positioning on the Pan.
    """

    pallet_id = db.Column(db.Integer, db.ForeignKey('pallet.id', ondelete="CASCADE", onupdate="CASCADE"),
                          nullable=False, primary_key=True)
    width_position = db.Column('Width Position', db.Integer, db.CheckConstraint('Width Position >= 0'), nullable=False)
    length_position = db.Column('Length Position', db.Integer, db.CheckConstraint('Length Position >= 0'),
                                nullable=False)
    height_position = db.Column('Height Position', db.Integer, db.CheckConstraint('Height Position >= 0'),
                                nullable=False)
    above_rail = db.Column('Rail', db.Boolean, nullable=False, default=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id', ondelete='CASCADE', onupdate='CASCADE'),
                            nullable=False, primary_key=True)
