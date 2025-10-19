from datetime import datetime
from app import db

class Panel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    panel_type = db.Column(db.String(50), nullable=False)  # cpanel, directadmin, plesk, etc.
    login_url = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # In production, encrypt this
    host_provider = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Panel {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'panel_type': self.panel_type,
            'login_url': self.login_url,
            'username': self.username,
            'host_provider': self.host_provider,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
