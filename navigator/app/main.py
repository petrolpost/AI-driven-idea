from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager
import pathlib
import markdown2

from . import models, database, crud, schemas

# --- Lifespan Management & App Initialization ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown events."""
    print("Initializing database...")
    database.init_db()
    print("Database initialized.")
    yield
    print("Application shutting down.")

app = FastAPI(lifespan=lifespan)

# --- Path Definitions ---

base_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
frontend_dir = base_dir.joinpath("frontend").resolve()
projects_dir = base_dir.joinpath("ideaed-projects").resolve()

# --- Static Files Mounting ---

if not frontend_dir.is_dir():
    raise RuntimeError(f"Frontend directory not found at: {frontend_dir}")
app.mount("/assets", StaticFiles(directory=frontend_dir), name="frontend_assets")

# --- API Endpoints ---

@app.get("/api/projects", response_model=List[schemas.Project])
def read_projects_api(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Retrieves a list of all projects from the database."""
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@app.post("/api/projects", response_model=schemas.Project)
def create_project_api(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    """Creates a new project in the database."""
    # Here you could add a check for existing readme_path to avoid duplicates
    return crud.create_project(db=db, project=project)

@app.get("/view/{file_path:path}")
async def view_project_file_as_html(file_path: str):
    """
    Finds a markdown file, converts it to HTML, and returns it for viewing.
    """
    full_path = base_dir.joinpath(file_path).resolve()

    if not str(full_path).startswith(str(projects_dir)):
        raise HTTPException(status_code=403, detail="Access denied.")
    
    if not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")

    content = full_path.read_text(encoding="utf-8")
    
    # Convert markdown to an HTML fragment
    html_fragment = markdown2.markdown(content, extras=["fenced-code-blocks", "tables"])

    # Build a full HTML document with the GitHub-like styling
    html_response_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{pathlib.Path(file_path).name}</title>
        <link rel="stylesheet" href="/assets/github-markdown.css">
        <style>
            body {{
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }}
        </style>
    </head>
    <body>
        <main class="markdown-body">
            {html_fragment}
        </main>
    </body>
    </html>
    """
    return HTMLResponse(content=html_response_content)

@app.get("/{full_path:path}")
async def serve_frontend_catch_all(full_path: str):
    """
    Serves the index.html for any non-API, non-static file path,
    enabling frontend routing.
    """
    index_path = frontend_dir.joinpath("index.html")
    if not index_path.is_file():
        raise HTTPException(status_code=500, detail="index.html not found.")
    return FileResponse(index_path)
