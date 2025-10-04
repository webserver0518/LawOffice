import os
from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')

def create_app(env='development'):
    if env == 'production':
        config_class = ProductionConfig
    else:
        config_class = DevelopmentConfig

    app = Flask(
        __name__,
        template_folder= template_dir,
        static_folder= static_dir)
    app.config.from_object(config_class)

    from .routes.site import site_bp
    from .routes.admin import admin_bp
    from .routes.client import client_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)

    @app.after_request
    def no_cache(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    return app
