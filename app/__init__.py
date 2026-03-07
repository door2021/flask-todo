import os
import logging
from flask import Flask, render_template
from .extensions import db, migrate, login_manager, mail, csrf

def create_app(config_class=None):

    if config_class is None:
        env = os.environ.get('FLASK_ENV', 'development')
        if env == 'production':
            from config import ProductionConfig
            config_class = ProductionConfig
        elif env == 'testing':
            from config import TestingConfig
            config_class = TestingConfig
        else:
            from config import DevelopmentConfig
            config_class = DevelopmentConfig
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config.get("DEBUG"):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        app.logger.setLevel(logging.DEBUG)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .home.home_routes import home
    from .auth.auth_routes import auth
    app.register_blueprint(auth)
    app.register_blueprint(home)

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.warning(f"404 error triggered: {e}")
        try:
            return render_template("404.html"), 404
        except Exception as template_error:
            app.logger.error(f"Failed to render 404.html: {template_error}", exc_info=True)
            return "404 - Page Not Found", 404

    return app