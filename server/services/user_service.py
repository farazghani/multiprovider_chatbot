from model import User, Userresponse
from db.db import get_db
import sqlite3
import datetime
import jwt
import uuid

SECRET_KEY = "super_secret_key_for_local_development_only"
ALGORITHM = "HS256"
DB_PATH = "app.db"

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

    def register_user(self, user: User) -> Userresponse:
        with get_db() as conn:
            try:
                user_id = str(uuid.uuid4())
                token = create_jwt(
                    user_id,
                    user.email
                )
                
                conn.execute("""
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
                conn.commit()
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
        with get_db() as conn:      
            try:
            
                user = conn.execute("""
                    SELECT id, email, password, jwt
                    FROM users
                    WHERE email = ?
                    """, (email,)).fetchone()
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
