from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai

router = APIRouter()
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

class ChatMessage(BaseModel):
    message: str

@router.get("/chat")
async def hello():
    return {"message": "hello"}

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
async def post_openai(chat_message: ChatMessage):

    client = openai.Client()
    # デバッグログの追加
    print(f"Received message: {chat_message.message}")

    try:
        # OpenAI APIリクエスト
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "親しみやすいAIです。何か質問があればどうぞ。"},
                {"role": "user", "content": chat_message.message}
            ]
            )
        print("OpenAI API request successful")

    except Exception as e:
        print(f"Error with OpenAI API request: {str(e)}")
        raise HTTPException(status_code=500, detail
        =str(e))
    response_text = response.choices[0].message
    return {"response": response_text}