from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Use a simple database path that works with Docker volumes
    db_path = '/app/data/webpanel_manager.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.views.main import main_bp
    from app.views.panels import panels_bp
    from app.views.backup import backup_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(panels_bp, url_prefix='/panels')
    app.register_blueprint(backup_bp, url_prefix='/backup')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
