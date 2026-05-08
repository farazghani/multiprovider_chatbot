import sqlite3
from db.db import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def addusers() -> dict[str , bool]:
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id          TEXT PRIMARY KEY NOT NULL,
            name        TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            jwt         TEXT NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return{"success on adding user_table": True}
    except Exception as e:
        print(e)
        return {"success_on_adding_users_table" : False}
    
    

def  add_chatmessages() -> dict[str , bool]:
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL CHECK (
            role IN ('system', 'user', 'assistant', 'tool')
        ),
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        provider TEXT,
        FOREIGN KEY (conversation_id)
            REFERENCES conversations(id)
            ON DELETE CASCADE
        );     
        """)
        conn.commit()
        return{"success on adding chatmessages_table": True}
    except Exception as e:
        print(e)
        return{"success on adding chatmessages_table": False}
    
    

def adding_conversations() -> dict[str , bool]:
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
        );
            
        """)
        conn.commit()
        return{"success on adding conversations table": True}
    except Exception as e:
        print(e)
        return{"success on adding conversations table": False}
    


if __name__ == "__main__":
    print(addusers())
    print(adding_conversations())
    print(add_chatmessages())

    
