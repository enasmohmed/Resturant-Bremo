from flask import Flask, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin

class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Meal:
    def __init__(self,id,name,photo_url,details,price):
        self.id = id
        self.name = name
        self.photo_url = photo_url
        self.details = details
        self.price = price

class Order:
    def __init__(self,id,name,address,phone,meal):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.meal = meal









