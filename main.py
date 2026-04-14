from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def greeting():
    return {"message": "Hello world!"}

@app.get("/welcome")
def greeting2():
    return {"message": "Hello world 2!"}

if __name__ ==  "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)