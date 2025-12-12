import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
csrf = CSRFProtect(app)

@app.get("/")
def index():
    return render_template('index.html')

@app.post("/")
def post_pwd_change():
    username = request.form['username']
    currentPassword = request.form['currentPassword']
    newPassword = request.form['newPassword']

    return render_template('index.html', successmsg="Password changed successfully, you can login to services with new password!")