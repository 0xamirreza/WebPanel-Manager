from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['VERSION'] = os.environ.get('VERSION', '1.0.0')
    
    # Use a simple database path that works with Docker volumes
    db_path = '/app/data/webpanel_manager.db'
    
    # Ensure data directory exists
    data_dir = os.path.dirname(db_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Context processor to make version available in all templates
    @app.context_processor
    def inject_version():
        return dict(version=app.config['VERSION'])
    
    # Register blueprints
    from app.views.main import main_bp
    from app.views.panels import panels_bp
    from app.views.backup import backup_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(panels_bp, url_prefix='/panels')
    app.register_blueprint(backup_bp, url_prefix='/backup')
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print(f"✅ Database initialized successfully at: {db_path}")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            print(f"📁 Data directory: {data_dir}")
            print(f"🔐 Directory permissions: {oct(os.stat(data_dir).st_mode)[-3:] if os.path.exists(data_dir) else 'N/A'}")
            raise
    
    return app
