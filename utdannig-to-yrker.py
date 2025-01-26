import sqlite3

def create_tables():
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create the Education table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    ''')

    # Create the Work table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Work (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    );
    ''')

    # Create the junction table for the many-to-many relationship
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EducationWork (
        education_id TEXT NOT NULL,
        work_id INTEGER NOT NULL,
        FOREIGN KEY (education_id) REFERENCES basic_studies (id) ON DELETE CASCADE,
        FOREIGN KEY (work_id) REFERENCES Work (id) ON DELETE CASCADE,
        PRIMARY KEY (education_id, work_id)
    );
    ''')

    # Commit changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")