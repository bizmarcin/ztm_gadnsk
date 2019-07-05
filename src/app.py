import sqlite3
from functools import wraps
from flask import Flask, render_template, request, session, redirect, flash, get_flashed_messages
from werkzeug.security import check_password_hash

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('ztm_map.html')


if __name__ == "__main__":
    app.run()