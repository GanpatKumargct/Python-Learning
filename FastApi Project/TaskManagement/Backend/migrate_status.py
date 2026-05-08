from sqlalchemy import text
from app.database.database import engine

try:
    with engine.begin() as conn:
        # Alter the column type to VARCHAR and convert existing boolean values
        conn.execute(text("ALTER TABLE tasks ALTER COLUMN status TYPE VARCHAR USING (CASE WHEN status=TRUE THEN 'completed' ELSE 'not completed' END);"))
        # Set the new default
        conn.execute(text("ALTER TABLE tasks ALTER COLUMN status SET DEFAULT 'not completed';"))
        print("Database schema successfully updated!")
except Exception as e:
    print("Could not update database schema, maybe it doesn't exist or is already updated. Error:", e)
