from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from services.models import User


class SignUpForm(FlaskForm):
    def validate_username(self, username_to_check):
        print('v1, username: ',username_to_check.data)
        user = User.getByUsername(username_to_check.data)
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email(self, email_to_check):
        print('v2, email: ',email_to_check.data)
        user = User.getByEmail(email_to_check.data)
        if user:
            raise ValidationError('Email Address already exists! Please try a different email address')

    name = StringField('Name:', validators=[Length(min=2, max=30), DataRequired()])
    username = StringField('Username:', validators=[Length(min=2, max=30), DataRequired()])
    email= StringField('Email:', validators=[Email(), DataRequired()])
    password = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    confirmPassword = PasswordField('Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Create Account')