from flask import render_template, url_for, flash, redirect, request
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm

class DetailForm(FlaskForm):
    state = StringField('State', validators=[DataRequired()])
    dates = StringField('Date',validators=[DataRequired(), Length(min=10, max=10)])
    options = StringField('Enter your Choice', validators=[DataRequired(), Length(min=1, max=1)])
    submit = SubmitField('Submit')