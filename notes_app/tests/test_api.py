import unittest
import json
from app import create_app, db
from app.models import Note, SharedNote
import os

class APITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        # Configure the app for testing
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:' # Use in-memory SQLite for tests
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing forms if any; not critical for JSON API
        self.client = self.app.test_client()

        # Create tables in the database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        # It's good practice to unset environment variables if they were set specifically for a test,
        # though for 'DATABASE_URL' here, it's set before create_app, so it's scoped to app instance.
        # If it were modified after app creation and affected global state, unsetting would be more critical.

    # Helper method to create a note directly for testing purposes
    def _create_note(self, title="Test Note", content="Test Content"):
        with self.app.app_context():
            note = Note(title=title, content=content)
            db.session.add(note)
            db.session.commit()
            return note

    # --- Test Cases for Notes API ---
    def test_create_note_api(self):
        """Test API can create a note (POST request)"""
        res = self.client.post('/api/notes', json={'title': 'Test Create', 'content': 'Content for create test'})
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertIn('Test Create', data['title'])
        self.assertTrue(data['id'] is not None)

    def test_create_note_api_missing_content(self):
        """Test API returns 400 if content is missing"""
        res = self.client.post('/api/notes', json={'title': 'Test No Content'})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('Missing content', data['error'])

    def test_get_all_notes_api(self):
        """Test API can get all notes (GET request)"""
        self._create_note(title="Note 1", content="Content 1")
        self._create_note(title="Note 2", content="Content 2")

        res = self.client.get('/api/notes')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['notes']), 2)
        self.assertEqual(data['notes'][0]['title'], 'Note 1')

    def test_get_single_note_api(self):
        """Test API can get a single note by its ID (GET request)"""
        note = self._create_note(title="Single Note", content="Content for single note")

        res = self.client.get(f'/api/notes/{note.id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['title'], 'Single Note')
        self.assertEqual(data['id'], note.id)

    def test_get_non_existent_note_api(self):
        """Test API returns 404 for a non-existent note ID"""
        res = self.client.get('/api/notes/9999')
        self.assertEqual(res.status_code, 404)

    def test_update_note_api(self):
        """Test API can update an existing note (PUT request)"""
        note = self._create_note()
        update_data = {'title': 'Updated Title', 'content': 'Updated Content'}

        res = self.client.put(f'/api/notes/{note.id}', json=update_data)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['content'], 'Updated Content')

        # Verify in DB
        with self.app.app_context():
            updated_note_db = Note.query.get(note.id)
            self.assertEqual(updated_note_db.title, 'Updated Title')

    def test_update_non_existent_note_api(self):
        """Test API returns 404 when updating a non-existent note"""
        res = self.client.put('/api/notes/9999', json={'title': 'Ghost Update'})
        self.assertEqual(res.status_code, 404)

    def test_delete_note_api(self):
        """Test API can delete an existing note (DELETE request)"""
        note = self._create_note()

        res = self.client.delete(f'/api/notes/{note.id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Note deleted successfully')

        # Verify it's deleted from DB
        with self.app.app_context():
            deleted_note_db = Note.query.get(note.id)
            self.assertIsNone(deleted_note_db)

    def test_delete_non_existent_note_api(self):
        """Test API returns 404 when deleting a non-existent note"""
        res = self.client.delete('/api/notes/9999')
        self.assertEqual(res.status_code, 404)

    # --- Test Cases for Sharing API ---
    def test_share_note_api(self):
        """Test API can create a share link for a note"""
        note = self._create_note()

        res = self.client.post(f'/api/notes/{note.id}/share')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertTrue(data['share_token'] is not None)
        self.assertTrue(data['share_url'] is not None)
        self.assertIn(data['share_token'], data['share_url'])

        # Verify SharedNote entry in DB
        with self.app.app_context():
            shared_note_db = SharedNote.query.filter_by(note_id=note.id).first()
            self.assertIsNotNone(shared_note_db)
            self.assertEqual(shared_note_db.unique_token, data['share_token'])

    def test_share_non_existent_note_api(self):
        """Test API returns 404 when trying to share a non-existent note"""
        res = self.client.post('/api/notes/9999/share')
        self.assertEqual(res.status_code, 404)

    def test_view_shared_note_api(self):
        """Test API can retrieve a note via its share token"""
        note = self._create_note(title="Shared Content Test", content="This is shared.")

        # First, create a share link
        share_res = self.client.post(f'/api/notes/{note.id}/share')
        self.assertEqual(share_res.status_code, 201)
        share_data = json.loads(share_res.data)
        token = share_data['share_token']

        # Now, view the note using the token
        res = self.client.get(f'/api/share/{token}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['title'], "Shared Content Test")
        self.assertEqual(data['content'], "This is shared.")

    def test_view_invalid_share_token_api(self):
        """Test API returns 404 for an invalid share token"""
        res = self.client.get('/api/share/invalid-token-uuid')
        self.assertEqual(res.status_code, 404)

    def test_welcome_message_api(self):
        """Test the welcome API endpoint"""
        res = self.client.get('/api/welcome')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['message'], "Welcome to the Notes API!")

if __name__ == '__main__':
    unittest.main()
