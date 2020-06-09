from flask_sqlalchemy import SQLAlchemy

DATABASE_PATH = "postgresql://postgres:135792468@localhost:5432/users"

db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
