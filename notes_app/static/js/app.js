document.addEventListener('DOMContentLoaded', function() {
    const noteForm = document.getElementById('note-form');
    const notesList = document.getElementById('notes');
    const API_BASE_URL = '/api'; // Using the new /api prefix

    // Function to fetch and display all notes
    async function fetchNotes() {
        try {
            const response = await fetch(`${API_BASE_URL}/notes`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            renderNotes(data.notes);
        } catch (error) {
            console.error('Error fetching notes:', error);
            notesList.innerHTML = '<li>Error loading notes. Please try again later.</li>';
        }
    }

    // Function to render notes in the list
    function renderNotes(notes) {
        if (!notes || notes.length === 0) {
            notesList.innerHTML = '<li>No notes yet. Create one!</li>';
            return;
        }
        notesList.innerHTML = ''; // Clear existing notes
        notes.forEach(note => {
            const listItem = document.createElement('li');
            listItem.dataset.id = note.id;
            listItem.innerHTML = `
                <h3>${escapeHTML(note.title) || 'Untitled Note'}</h3>
                <p>${escapeHTML(note.content)}</p>
                <small>Created: ${new Date(note.created_at).toLocaleString()}</small>
                ${note.updated_at ? `<br><small>Updated: ${new Date(note.updated_at).toLocaleString()}</small>` : ''}
                <div class="actions">
                    <button class="share-btn" data-id="${note.id}">Share</button>
                    <button class="delete-btn" data-id="${note.id}">Delete</button>
                </div>
            `;
            notesList.appendChild(listItem);
        });
    }

    // Handle new note creation
    if (noteForm) {
        noteForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;

            if (!content.trim()) {
                alert('Content cannot be empty!');
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/notes`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title, content }),
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                }
                // const newNote = await response.json(); // Contains id, title, content, message
                fetchNotes(); // Refresh the list
                noteForm.reset(); // Clear the form
            } catch (error) {
                console.error('Error creating note:', error);
                alert(`Error creating note: ${error.message}`);
            }
        });
    }

    // Handle delete and share actions (using event delegation)
    if (notesList) {
        notesList.addEventListener('click', async function(event) {
            const target = event.target;
            const noteId = target.dataset.id;

            if (target.classList.contains('delete-btn')) {
                if (!confirm('Are you sure you want to delete this note?')) return;
                try {
                    const response = await fetch(`${API_BASE_URL}/notes/${noteId}`, {
                        method: 'DELETE',
                    });
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                    }
                    fetchNotes(); // Refresh the list
                } catch (error) {
                    console.error('Error deleting note:', error);
                    alert(`Error deleting note: ${error.message}`);
                }
            }

            if (target.classList.contains('share-btn')) {
                try {
                    const response = await fetch(`${API_BASE_URL}/notes/${noteId}/share`, {
                        method: 'POST',
                    });
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                    }
                    const shareData = await response.json();
                    prompt("Share this link:", shareData.share_url);
                } catch (error) {
                    console.error('Error sharing note:', error);
                    alert(`Error sharing note: ${error.message}`);
                }
            }
        });
    }

    // Utility to escape HTML to prevent XSS
    function escapeHTML(str) {
        if (str === null || str === undefined) return '';
        return str.toString()
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Initial fetch of notes
    fetchNotes();
});
