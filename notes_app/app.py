from app import create_app, db

app = create_app()

@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    with app.app_context():
        db.create_all()
    print("Initialized the database and created tables.")

if __name__ == '__main__':
    # The app context is available here if create_app() is called before app.run()
    # For development, it's common to ensure tables are there.
    # However, using the 'flask init-db' command is cleaner.
    app.run(debug=True)
