from flask import Flask


app = Flask(__name__)
app.secret_key='172.17.0.19'
from .server import *
