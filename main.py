from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from utils.github_loader import clone_repo, get_repo_id
from fastapi import BackgroundTasks, HTTPException
from utils.file_loader import load_files
from utils.vector_database import create_vector_store, load_vector_store

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

repo_status = {}

class ProcessRequest(BaseModel):
    repo_url: str

@app.get("/")
def greeting():
    return {"message": "Hello world!"}

@app.post("/api/process")
async def process_repository(request: ProcessRequest, background_tasks: BackgroundTasks):
    repo_url = request.repo_url
    try:
        repo_id = get_repo_id(repo_url)
        repo_status[repo_id] = "processing"

        # Run the heavy processing in the background
        background_tasks.add_task(run_indexing, repo_url, repo_id)
        
        return {"repo_id" : repo_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=(str(e)))
    
def run_indexing(repo_url, repo_id):
    try:
        path = clone_repo(repo_url)
        docs = load_files(path)
        db = create_vector_store(docs, repo_id)
        repo_status[repo_id] = "completed"
    except Exception as e:
        print(f"Erro indexing {repo_id}: {e}")
        repo_status[repo_id] = f"failed: {str(e)}"
    
if __name__ ==  "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)