from flask import Blueprint, jsonify, request, url_for, render_template # Added render_template
from .models import Note, SharedNote
from . import db

main_bp = Blueprint('main', __name__)

# --- HTML Serving Routes ---
@main_bp.route('/')
def serve_index():
    return render_template('index.html')

@main_bp.route('/shared/<string:token>') # This route serves the HTML page
def serve_shared_note_page(token):
    # We can pass the token to the template if needed, or let JS handle fetching
    return render_template('view_note.html', token=token)

# --- API Endpoints (already defined, ensuring they are part of the file) ---
@main_bp.route('/api/welcome') # Renamed original / to /api/welcome to avoid conflict
def index(): # Renamed function to avoid conflict
    return jsonify(message="Welcome to the Notes API!")

@main_bp.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    if not data or not 'content' in data:
        return jsonify(error="Missing content for note"), 400
    new_note = Note(title=data.get('title'), content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify(id=new_note.id, title=new_note.title, content=new_note.content, message="Note created successfully"), 201

@main_bp.route('/api/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    output = []
    for note in notes:
        note_data = {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat() if note.created_at else None,
            'updated_at': note.updated_at.isoformat() if note.updated_at else None
        }
        output.append(note_data)
    return jsonify(notes=output)

@main_bp.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    return jsonify(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at.isoformat() if note.created_at else None,
        updated_at=note.updated_at.isoformat() if note.updated_at else None
    )

@main_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    if not data: return jsonify(error="No data provided for update"), 400
    if 'title' in data: note.title = data['title']
    if 'content' in data: note.content = data['content']
    db.session.commit()
    return jsonify(id=note.id, title=note.title, content=note.content, message="Note updated successfully")

@main_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify(message="Note deleted successfully"), 200

@main_bp.route('/api/notes/<int:note_id>/share', methods=['POST'])
def share_note(note_id):
    note = Note.query.get_or_404(note_id)
    shared_link = SharedNote(note_id=note.id)
    db.session.add(shared_link)
    db.session.commit()
    # The 'serve_shared_note_page' is the new HTML page route
    # The 'view_shared_note_api' is the API endpoint for fetching shared note data
    share_page_url = url_for('main.serve_shared_note_page', token=shared_link.unique_token, _external=True)
    return jsonify(
        message="Note shared successfully. Share this URL with others.",
        share_token=shared_link.unique_token,
        share_url=share_page_url # This is the URL to the HTML page
    ), 201

@main_bp.route('/api/share/<string:token>', methods=['GET']) # This is the API endpoint for shared note data
def view_shared_note_api(token): # Renamed to avoid conflict with HTML serving route
    shared_link = SharedNote.query.filter_by(unique_token=token).first_or_404()
    note = Note.query.get_or_404(shared_link.note_id)
    return jsonify(
        title=note.title,
        content=note.content,
        shared_at=shared_link.created_at.isoformat() if shared_link.created_at else None
    )
