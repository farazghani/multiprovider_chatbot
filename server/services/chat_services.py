from model import ChatMessage, Conversation
from db.db import get_db
import sqlite3

class ConversationService:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

    def create_conversation(self, title: str) -> dict:
        conversation = Conversation(
            title=title,
            user_id=self.user_id
        )
        try:
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO conversations (id, user_id, title)
                    VALUES (?, ?, ?)
                """, (conversation.id, conversation.user_id, conversation.title))
                conn.commit()
            return {"success": True, "conversation_id": conversation.id}
        except sqlite3.IntegrityError as e:
            print(e)
            return {"success": False}

    def create_chat(self, content: str, conversation_id: str, provider: str, role: str) -> dict:
        chat = ChatMessage(
            role=role,
            content=content,
            conversation_id=conversation_id,
            provider=provider
        )
        try:
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO chat_messages (id, conversation_id, role, content, provider)
                    VALUES (?, ?, ?, ?, ?)
                """, (chat.id, chat.conversation_id, chat.role, chat.content, chat.provider))
                conn.commit()
            return {"success": True, "message_id": chat.id}
        except sqlite3.IntegrityError as e:
            print(e)
            return {"success": False , "error": e}   

if __name__ == "__main__":
    service = ConversationService(user_id="868b32da-1ac4-4a1c-b4a9-e65c9b56b759")

    result = service.create_conversation(title="my first chat")
    print(result)

       # test create chat using the conversation id we just made
    if result["success"]:
        conv_id = result["conversation_id"]

        msg1 = service.create_chat(
            content="hello, how do i fix a global cursor bug?",
            conversation_id=conv_id,
            provider="claude",
            role="user"
        )
        print("create user message:", msg1)

        msg2 = service.create_chat(
            content="a global cursor is not thread safe...",
            conversation_id=conv_id,
            provider="claude",
            role="assistant"
        )
        print("create assistant message:", msg2)