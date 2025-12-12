import os
from ldap3 import Server, Connection, ALL
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),
    **os.environ
}

# Some sane default fallback values
if not "LDAP_HOST" in config:
    config["LDAP_HOST"] = '127.0.0.1'
if not "LDAP_PORT" in config:
    config["LDAP_PORT"] = 3389
if not "USER_BIND_TMPL" in config:
    config["USER_BIND_TMPL"] = "cn=%s,ou=people,cn=example,cn=ee"

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
    app.logger.info(f"Changing password for user '{username}'")

    try:
        try:
            server = Server(config['LDAP_HOST'], port=int(config['LDAP_PORT']), get_info=ALL)
        except Exception as e:
            app.logger.error(f"Failed to establish LDAP connection: {e}")
            return render_template('index.html', errmsg="Internal server error"), 500

        # TODO: Replace it with a template read from dotenv and do escaping
        dn = config["USER_BIND_TMPL"] % username
        conn = Connection(server, user=dn, password=currentPassword, auto_bind=True)
        if not conn.bind():
            return render_template('index.html', errmsg="Internal server error"), 500
        conn.extend.standard.modify_password(dn, currentPassword, newPassword)
        return render_template('index.html', successmsg="Password changed successfully, you can login to services with new password!")
    except Exception as e:
        app.logger.warning(f"Failed to change password for user '{username}': {e}")
        return render_template('index.html', errmsg="Invalid username or password"), 400