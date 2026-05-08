from model import User, Userresponse
from db.db import DB_PATH
import sqlite3
import datetime
import jwt
import uuid

SECRET_KEY = "super_secret_key_for_local_development_only"
ALGORITHM = "HS256"


def create_jwt(user_id: str, email: str) -> str:
    payload = {
        "id": user_id,
        "email": email,
        "exp": datetime.datetime.now() + datetime.timedelta(days=1)
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


class Auth:

    def __init__(self, db: str):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self._ensure_users_table()

    def _ensure_users_table(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id          TEXT PRIMARY KEY NOT NULL,
                name        TEXT NOT NULL,
                email       TEXT UNIQUE NOT NULL,
                password    TEXT NOT NULL,
                jwt         TEXT NOT NULL,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def register_user(self, user: User) -> Userresponse:

        try:
            user_id = str(uuid.uuid4())
            token = create_jwt(
                user_id,
                user.email
            )
            self.cursor.execute("""
                INSERT INTO users(
                    id,
                    name,
                    email,
                    password,
                    jwt
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id,
                user.name,
                user.email,
                user.password,
                token
            ))
            self.conn.commit()
            return Userresponse(
                id=user_id,
                jwt=token,
                success=True
            )
        except sqlite3.IntegrityError as e:
           return Userresponse(
                success=False,
                error= str(e)
            )

    def signin_user(
        self,
        email: str,
        password: str
    ) -> Userresponse:
        try:
            self.cursor.execute("""
                SELECT id, email, password, jwt
                FROM users
                WHERE email = ?
            """, (email,))
            user = self.cursor.fetchone()
            if not user:
                return Userresponse(
                    success=False
                )
            db_id, db_email, db_password, db_jwt = user
            if password != db_password:
                return Userresponse(
                    success=False
                )
            return Userresponse(
                id=db_id,
                jwt=db_jwt,
                success=True
            )
        except sqlite3.Error as e:
            return Userresponse(
                success=False,
                error= str(e)
            )


if __name__ == "__main__":
    auth = Auth(str(DB_PATH))

    data = User(
        id=str(uuid.uuid4()),
        name="Faraz",
        email="farazghani973@gmail.com",
        password="clamentine123"
    )


    response = auth.signin_user("farazghani973@gmail.com" , "clamentine123")
    print(response)
