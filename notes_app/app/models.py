from . import db # Import db from the current package (app)
from sqlalchemy.sql import func
import uuid # For generating unique tokens

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationship to shared notes (one-to-many)
    shared_links = db.relationship('SharedNote', backref='note', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Note {self.id}: {self.title[:30]}>'

class SharedNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    unique_token = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<SharedNote token: {self.unique_token}>'
