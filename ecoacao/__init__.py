import os
import secrets
from pathlib import Path

from flask import Flask

from ecoacao.db import close_db, init_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "ecoacao.sqlite3"),
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
    )

    if test_config is not None:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from ecoacao.routes import bp

    app.register_blueprint(bp)
    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()

    return app
