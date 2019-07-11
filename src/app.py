import sqlite3
from functools import wraps
from flask import Flask, render_template, request, session, redirect, flash, get_flashed_messages
from werkzeug.security import check_password_hash
from ztm_gdansk import map
app = Flask(__name__)
import folium

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()