from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException
from dotenv import load_dotenv

import os


router = APIRouter()
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

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

@router.post("/openai")
# 受け取ったメッセージをOpenAIに送信して、返答を返す
async def post_openai(chat_message: ChatMessage):    
    response_message = f"Received message: {chat_message.message}"
    
    # デバッグログの追加
    print(f"Received message: {chat_message.message}")
    # 受け取ったメッセージをOpenAIに送信して、返答を返す

    try:
        import openai
        response = openai.Completion.create(
            engine="davinci",
            prompt=chat_message.message,
            max_tokens=100,
            api_key=openai_api_key
        )

        response_message = response.choices[0].text
    except Exception as e:
        print(f"Error with OpenAI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"response": response_message}
