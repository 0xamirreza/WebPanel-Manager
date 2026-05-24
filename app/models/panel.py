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
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
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
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'remaining_days': self.remaining_days,
            'created_at': self.created_at.isoformat()
        }

    @property
    def remaining_days(self):
        if not self.start_date or not self.end_date:
            return None
        return (self.end_date - self.start_date).days
