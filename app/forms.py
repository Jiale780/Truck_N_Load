from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import User, Delivery, Customer, Pan


class LoginForm(FlaskForm):
    """ This is the form that is used to login users """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """ This is the form that is used to create new users """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create User')

    def validate_username(self, username):
        """ This is added as a validator for WTForms to prevent the same username as an existing user """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        """ This is added as a validator for WTForms to prevent the same email as an existing user """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address is already in use')


class PanCreationForm(FlaskForm):
    """ This is the form that is used to create new pans """
    weight = FloatField('Max Weight (Kg)', validators=[DataRequired(message='Must be a number'), NumberRange(min=0)])
    height = FloatField('Height (Meters)', validators=[DataRequired(message='Must be a number'), NumberRange(min=0)])
    width = FloatField('Width (Meters)', validators=[DataRequired(message='Must be a number'), NumberRange(min=0)])
    length = FloatField('Length (Meters)', validators=[DataRequired(message='Must be a number'), NumberRange(min=0)])
    rail_height = FloatField('Rail Height (Meters)', validators=[DataRequired(message='Must be a number'), NumberRange(min=0)])
    cost = FloatField('Cost ($)', validators=[DataRequired(message='Must be a number'), NumberRange(min=0)])
    submit = SubmitField('Create Pan')


class PalletCreationForm(FlaskForm):
    """ This is the form that is used to create new pallets"""
    weight = FloatField('Weight (Kg)', validators=[DataRequired(message='Must be a number'), NumberRange(min=0)])
    height = FloatField('Height (Meters)', validators=[DataRequired(message='Must be a number'), NumberRange(min=0)])
    can_stack = SelectField('Can Stack', choices=[(True, 'True'), (False, 'False')], coerce=bool)
    category = SelectField('Category', choices=[('D', 'Dry'), ('C', 'Chiller'), ('F', 'Frozen')])
    customer = SelectField('Customer', choices=[(c.id, str(c.first_name+": "+c.address)) for c in Customer.query], coerce=int)
    delivery_id = HiddenField('delivery_id')  # This is set before delivering the form to a user
    submit = SubmitField('Create Pallet')


class DeliverySelectorForm(FlaskForm):
    """ This is a form that is used to select a delivery """
    delivery_id = SelectField('Delivery ID', choices=(
        [(d.id, ("ID: {}, Address: {}".format(d.id, d.address))) for d in Delivery.query]), coerce=int)
    submit = SubmitField('Submit')


class DeliveryCreationForm(FlaskForm):
    """ This is a form that is used to create new deliveries (runs) """
    address = StringField('Address', validators=[DataRequired()])
    pan_id = SelectField('Pan', choices=[
        (p.id,
         ('Length: {}, Width: {}, Height: {}, Cost: ${}'.format(p.length, p.width, p.height, p.cost))
         ) for p in Pan.query], coerce=int)
    submit = SubmitField('Create Delivery')


class CustomerCreationForm(FlaskForm):
    """ This is a form that is used to create new customers """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    submit = SubmitField('Create Customer')


class ManifestForm(FlaskForm):
    id = SelectField('Delivery', validators=[DataRequired(message="Must Select One")], coerce=int)
    id.choices = [row.id for row in Delivery.query.all()]
    submit = SubmitField("Submit")
