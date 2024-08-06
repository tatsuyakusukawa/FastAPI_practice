from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "hello world!"}

@app.get("/hoge")
async def hoge():
    return {"message": "hello hoge"}

