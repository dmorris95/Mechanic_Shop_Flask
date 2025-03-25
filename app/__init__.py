from flask import Flask
from app.models import db
from app.extensions import ma, limiter, cache
from app.blueprints.customers import customers_bp 
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import tickets_bp
from app.blueprints.inventory import inventory_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")
    
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    #registering blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app