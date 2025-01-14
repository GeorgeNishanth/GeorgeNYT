from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import yt_dlp

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Directory to serve HTML
cur_dir = os.getcwd()

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    """Serve the frontend HTML page."""
    html_path = os.path.join(cur_dir, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    raise HTTPException(status_code=404, detail="Frontend HTML file not found.")

@app.post("/download")
def download_video(link: str = Form(...)):
    """Handle video download requests."""
    try:
        youtube_dl_options = {
            "format": "best",  # Selects the best quality available
            "outtmpl": os.path.join(cur_dir, f"Video-{link[-11:]}.mp4"),
        }
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])
        return {"status": "Download started"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
