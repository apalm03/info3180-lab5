from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired,Email
from flask_wtf.file import FileAllowed, FileRequired, FileField 
from flask import Flask, render_template, flash, session, redirect, url_for
from wtforms import TextAreaField, TextField, SubmitField, SelectField

class UserProfileForm(FlaskForm):
    fname = StringField("First Name", validators=[InputRequired()])
    lname = StringField("Last Name", validators=[InputRequired()])
    gender = SelectField("Gender", choices=[("None", "Select Gender"), ("Male", "Male"), ("Female", "Female")], validators=[InputRequired()])
    email = StringField("Email", validators = [InputRequired(), Email()])
    location = StringField("Location", validators = [InputRequired()])
    bio = TextAreaField("Biography", validators = [InputRequired()])
    photo = FileField("Profile Picture", validators=[FileRequired(), FileAllowed(['jpg','png','jpeg'], 'Only image files accepted.')])    
    submit = SubmitField("Add Profile")