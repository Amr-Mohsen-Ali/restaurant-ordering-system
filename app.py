from pathlib import Path

from src import create_app, database

app = create_app()

# Staff-side persistence. Initialised only when running the server —
# tests that import create_app() are unaffected and can opt into the
# `db` pytest fixture to spin up their own isolated database.
DB_PATH = Path(__file__).parent / "src" / "data" / "restaurant.db"
database.init_db(DB_PATH)

if __name__ == '__main__':
    app.run(debug=True)