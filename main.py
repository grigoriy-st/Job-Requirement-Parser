import requests
import json
import csv
import time

import datetime
import sqlalchemy
import logging

from data import db_session

from flask import jsonify, Flask, render_template, redirect
from flask_restful import reqparse, abort, Api, Resource

from flask_login import (LoginManager, login_user,
                         login_required, logout_user,
                         current_user)

from api.users_api import users_api

# Models
from models.users import User

# Handlers
from handlers.work_with_users import work_with_users_bp
from handlers.auth import auth_bp
from handlers.work_with_analyzer import work_with_analyzer_bp

logging.basicConfig(level=logging.INFO)

db_session.global_init("db/database.sqlite")

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# Blueprints
app.register_blueprint(work_with_users_bp)
app.register_blueprint(users_api)
app.register_blueprint(auth_bp)
app.register_blueprint(work_with_analyzer_bp)

login_manager = LoginManager()
login_manager.init_app(app)

from collections import defaultdict
from pprint import pprint

from typing import Optional, Dict, Any  # Для аннотаций



@app.route('/main')
def get_main_page():
    return render_template('main_page.html')

def main():
    ...
@app.route('/users')
def get_users():
    db_ss = db_session.create_session()
    users = db_ss.query(User).all()
    return render_template("user_list.html", users=users)  


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return 'Вы не авторизованы. Пожалуйста перейдите по <a href="/login">ссылке</a> для авторизации.'


if __name__ == '__main__':
    app.run(port="8080", host="127.0.0.1", debug=True)
    main()
