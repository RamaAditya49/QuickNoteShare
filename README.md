# Notes App - Aplikasi Catatan Keren!

**Sebuah aplikasi web untuk membuat, mengelola, dan berbagi catatan dengan mudah. Proyek ini bersifat open-source dan kami mengundang siapa saja untuk berkontribusi dan mengembangkannya bersama!** (A web application to easily create, manage, and share notes. This project is open-source, and we invite everyone to contribute and develop it together!)

This Notes App allows users to create text-based notes, edit them, and share them via unique, read-only links. It's built with Python (Flask) on the backend and vanilla JavaScript on the frontend.

## Features

*   **Create Notes**: Easily write and save new notes with a title and content.
*   **View All Notes**: See a list of all your created notes.
*   **Edit Notes**: (Currently via API, UI for editing can be a future enhancement) Modify existing notes.
*   **Delete Notes**: Remove notes you no longer need.
*   **Share Notes**: Generate a unique, read-only link for any note to share with others.
*   **View Shared Notes**: Anyone with the unique link can view the note content without needing to log in.
*   **RESTful API**: A well-defined API for programmatic access to notes.

## Tech Stack

*   **Backend**:
    *   Python 3
    *   Flask (Web Framework)
    *   Flask-SQLAlchemy (ORM for database interaction)
    *   SQLite (Default database, easily configurable)
*   **Frontend**:
    *   HTML5
    *   CSS3
    *   Vanilla JavaScript (for dynamic content and API interaction)
*   **Testing**:
    *   Python `unittest` (for backend API tests)

## Project Structure

```
notes_app/
├── app/                    # Main Flask application package
│   ├── __init__.py         # Initializes Flask app and extensions
│   ├── models.py           # SQLAlchemy database models
│   ├── routes.py           # API and HTML serving routes
│   └── static/             # Static files (CSS, JavaScript, images)
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── app.js      # JS for the main notes page
│           └── view.js     # JS for the shared note view page
│   └── templates/          # HTML templates
│       ├── base.html       # Base template for others to extend
│       ├── index.html      # Main page for listing/creating notes
│       └── view_note.html  # Page for displaying a shared note
├── instance/               # Instance folder (e.g., for SQLite DB)
│   └── notes_app.db        # SQLite database file (created after init)
├── tests/                  # Backend tests
│   ├── __init__.py
│   └── test_api.py         # API test cases
├── .flaskenv               # Environment variables for Flask CLI
├── app.py                  # Entry point to run the Flask application
├── requirements.txt        # Python dependencies
├── LICENSE                 # Project License (MIT)
└── README.md               # This file
```

## Setup and Installation

Follow these steps to get the Notes App running on your local machine.

**1. Prerequisites:**
*   Python 3.7+
*   `pip` (Python package installer)
*   `git` (for cloning the repository)

**2. Clone the Repository:**
```bash
git clone <repository_url>  # Replace <repository_url> with the actual URL
cd notes-app-project-directory # Navigate to the project directory
```

**3. Create and Activate a Virtual Environment:**
It's highly recommended to use a virtual environment to manage project dependencies.

*   For Unix/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   For Windows:
    ```bash
    python -m venv venv
    .+env\Scriptsctivate
    ```

**4. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**5. Configure Environment Variables:**
The `.flaskenv` file is included with basic settings (`FLASK_APP=app.py`, `FLASK_ENV=development`). The database URL defaults to an SQLite database in the `instance` folder. No immediate changes are needed for default setup.

**6. Initialize the Database:**
This command will create the necessary database tables based on the models.
```bash
flask init-db
```
You should see a message "Initialized the database and created tables." and an `instance/notes_app.db` file will be created.

**7. Run the Application:**
```bash
flask run
```
The application will typically be available at `http://120.0.0.1:5000/`.

You can also run it directly (though `flask run` is preferred for development):
```bash
python notes_app/app.py
```

## Running Tests

To run the backend API tests:
Navigate to the project's root directory (where `notes_app` folder and `requirements.txt` are located).
Ensure your virtual environment is activated.

```bash
python -m unittest discover -s notes_app/tests -p "test_*.py"
```
Or, if you are in the `notes_app` parent directory:
```bash
python -m unittest discover -s ./notes_app/tests -p "test_*.py"
```

## API Endpoints Overview

The application provides the following API endpoints (all prefixed with `/api`):

*   `GET /api/welcome`: Welcome message.
*   `POST /api/notes`: Create a new note.
    *   Body: `{ "title": "Optional Title", "content": "Note content (required)" }`
*   `GET /api/notes`: Get all notes.
*   `GET /api/notes/<note_id>`: Get a specific note.
*   `PUT /api/notes/<note_id>`: Update a specific note.
    *   Body: `{ "title": "New Title", "content": "New Content" }`
*   `DELETE /api/notes/<note_id>`: Delete a specific note.
*   `POST /api/notes/<note_id>/share`: Generate a shareable link for a note.
*   `GET /api/share/<token>`: Get content of a shared note (used by the frontend for shared view).

## Contributing - Mari Berkontribusi!

Kami sangat senang jika Anda ingin berkontribusi pada proyek ini! (We are very happy if you want to contribute to this project!) Whether it's reporting a bug, suggesting a new feature, improving documentation, or writing code, all contributions are welcome.

**Cara Berkontribusi (How to Contribute):**

1.  **Fork the Repository**: Start by forking this repository to your own GitHub account.
2.  **Clone Your Fork**: Clone your forked repository to your local machine.
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_FORK_NAME.git
    ```
3.  **Create a New Branch**: Make your changes in a new git branch.
    ```bash
    git checkout -b my-feature-branch
    ```
4.  **Make Your Changes**: Implement your feature or fix the bug.
    *   Write clean code.
    *   Ensure your changes do not break existing functionality.
    *   **Add tests!** If you add new backend features, please include tests. Contributions for frontend tests (e.g., using Selenium, Cypress, or Playwright) would be especially appreciated!
5.  **Commit Your Changes**:
    ```bash
    git commit -m "feat: Describe your amazing feature" -m "Detailed description of changes."
    ```
    (Consider using [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.)
6.  **Push to Your Fork**:
    ```bash
    git push origin my-feature-branch
    ```
7.  **Open a Pull Request (PR)**: Go to the original repository and open a Pull Request from your forked branch. Provide a clear description of your changes in the PR.

**Reporting Issues or Suggesting Features:**
Use the "Issues" tab in the GitHub repository to report bugs or suggest new features. Please be as detailed as possible.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ayo buat aplikasi ini makin keren dan bermanfaat untuk semua!** (Let's make this application even cooler and more useful for everyone!)
