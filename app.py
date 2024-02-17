from flask import Flask
from util import util
from config import config
from datetime import timedelta
from blueprints.api import api as bp_api
from blueprints.template import app as bp_template


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = util.get_random_md5()
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_template)

    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0", port=config['port'])
