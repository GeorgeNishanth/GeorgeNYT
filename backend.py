from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
import os
import yt_dlp

app = FastAPI()

# Get the current directory of the project
cur_dir = os.getcwd()

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    """Serve the frontend HTML file."""
    html_path = os.path.join(cur_dir, "frontend.html")
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
