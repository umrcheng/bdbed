from flask import Blueprint, render_template, redirect, session, abort
from util import util
from util.sql import Sql
from config import config

app = Blueprint("bp_template", __name__)
sql = Sql()


@app.route('/')
def index():
    
    return abort(404)


@app.route(f'/{config["confound"]}/')
def admin_index():
    
    if not util.is_login(session):
        
        return redirect("/admin/login", 302)

    sql.connect("util/sql")
    count = sql.get_photo_length()
    sql.close()

    return render_template("index.html", count=count)


@app.route(f'/{config["confound"]}/login')
def admin_login():
    
    if util.is_login(session):
        
        return redirect("/admin", 302)
    return render_template("login.html")


@app.route(f'/{config["confound"]}/types')
def admin_types():
    
    if not util.is_login(session):
        
        return redirect("/admin/login", 302)
    return render_template("types.html")


@app.route(f'/{config["confound"]}/upload')
def admin_upload():
    
    if not util.is_login(session):
        
        return redirect("/admin/login", 302)

    return render_template("upload.html")


@app.route(f'/{config["confound"]}/permissions')
def admin_permissions():
    
    if not util.is_login(session):
        
        return redirect("/admin/login", 302)

    return render_template("permissions.html")
