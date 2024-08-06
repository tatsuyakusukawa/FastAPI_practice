from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException
import os



router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.get("/chat")
async def hello():
    return {"messege":"hello"}

@router.post("/chat")
async def post_chat(chat_message: ChatMessage):
    response_message = f"Received message: {chat_message.message}"
    
    # デバッグログの追加
    print(f"Received message: {chat_message.message}")
    
    try:
        # 絶対パスの使用
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'chat_msg.txt'))
        print(f"Writing to file: {file_path}")  # ファイルパスの確認
        
        with open(file_path, "a") as f:
            f.write(chat_message.message + "\n")
            print("Message written to file")  # 書き込み成功ログ
    except Exception as e:
        print(f"Error writing to file: {str(e)}")  # エラーログ
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"response": response_message}
