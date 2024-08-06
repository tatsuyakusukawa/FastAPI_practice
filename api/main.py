from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api.routers import chat

app = FastAPI()

app.include_router(chat.router)

# CORS設定
origins = [
    "http://127.0.0.1:5500",  # フロントエンドのオリジンを指定
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

    