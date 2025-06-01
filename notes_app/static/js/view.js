document.addEventListener('DOMContentLoaded', function() {
    const noteTitleElement = document.getElementById('note-title');
    const noteContentElement = document.getElementById('note-content');
    const noteSharedAtElement = document.getElementById('note-shared-at');
    const API_BASE_URL = '/api'; // Using the new /api prefix

    // Function to get token from URL path (e.g. /shared/<token>)
    function getShareTokenFromPath() {
        const pathSegments = window.location.pathname.split('/');
        // Assuming URL is /shared/TOKEN_VALUE, token is the last segment
        if (pathSegments.length > 0 && pathSegments[pathSegments.length - 2] === 'shared') {
            return pathSegments[pathSegments.length - 1];
        }
        return null;
    }

    async function fetchSharedNote() {
        const token = getShareTokenFromPath();

        if (!token) {
            noteTitleElement.textContent = 'Error';
            noteContentElement.textContent = 'Share token not found in URL.';
            return;
        }

        if (!noteTitleElement || !noteContentElement || !noteSharedAtElement) {
            console.error('One or more HTML elements for displaying the note are missing.');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/share/${token}`);
            if (!response.ok) {
                 if (response.status === 404) {
                    noteTitleElement.textContent = 'Note Not Found';
                    noteContentElement.textContent = 'This shared note could not be found or may have been deleted.';
                } else {
                    noteTitleElement.textContent = 'Error';
                    noteContentElement.textContent = `Could not load shared note. Status: ${response.status}`;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const note = await response.json();

            noteTitleElement.textContent = escapeHTML(note.title) || 'Untitled Note';
            noteContentElement.textContent = escapeHTML(note.content);
            if (note.shared_at) {
                noteSharedAtElement.textContent = `Shared on: ${new Date(note.shared_at).toLocaleString()}`;
            } else {
                noteSharedAtElement.textContent = '';
            }

        } catch (error) {
            console.error('Error fetching shared note:', error);
            // Error message already set in the if(!response.ok) block for specific cases
            if (noteTitleElement.textContent === 'Loading title...') { // Generic error if not already set
                noteTitleElement.textContent = 'Error';
                noteContentElement.textContent = 'Could not load shared note. Please check the link or try again later.';
            }
        }
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

    fetchSharedNote();
});
