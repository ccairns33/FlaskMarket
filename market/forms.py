from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    # validation from FlaskForm
    def validate_username(self, username_to_check):
        # if there is a user with username
        user = User.query.filter_by(username=username_to_check.data).first()
        # print(username_to_check) = <input id="username" maxlength="30" minlength="2" name="username" required type="text" value="CC">
        if user:
            raise ValidationError("Username already exists! Please choose a different username.")

    def validate_email(self, email_address_to_check):
        # if there is a user with username
        email = User.query.filter_by(email=email_address_to_check.data).first()
        if email:
            raise ValidationError("This email is in use. Please try a different email or Sign In.")

    username = StringField(label="Username:", validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label="Email:", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators= [EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Create Account")


