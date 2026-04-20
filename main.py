from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from utils.github_loader import clone_repo

app = FastAPI()

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ProcessRequest(BaseModel):
    repo_url: str

@app.get("/")
def greeting():
    return {"message": "Hello world!"}

@app.post("/api/process")
def process(request: ProcessRequest):
    clone_repo(request.repo_url)
    return {"Cloned Successfully"}
    

if __name__ ==  "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)