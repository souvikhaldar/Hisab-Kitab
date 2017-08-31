from src import app
from flask import jsonify, request
import requests
import json
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
#from flask_mysqldb import MySQL
#from data import Articles
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,IntegerField
#from passlib.hash import sha256_crypt
from functools import wraps


@app.route("/")
def index():
    return render_template("home.html")
