from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import io
import zipfile
from .scraper import RedditScraper

app = FastAPI(title="Reddit Media Scraper")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Initialize scraper
scraper = RedditScraper()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/scrape")
async def scrape(
    request: Request,
    reddit_url: str = Form(...),
    sort_by: str = Form(...),
    post_limit: int = Form(...)
):
    try:
        # Validate URL
        if not reddit_url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid URL format")
            
        # Validate post limit
        if not 1 <= post_limit <= 30:
            raise HTTPException(status_code=400, detail="Post limit must be between 1 and 30")
            
        # Get media files
        media_files = await scraper.scrape(reddit_url, sort_by, post_limit)
        
        if not media_files:
            raise HTTPException(status_code=404, detail="No media files found")

        # Create zip file with progress tracking
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, file in enumerate(media_files, 1):
                scraper.progress["current_action"] = f"Compressing file {i}/{len(media_files)}"
                zip_file.writestr(file['filename'], file['content'])
        
        zip_buffer.seek(0)
        
        # Generate filename from subreddit
        subreddit = reddit_url.split('/r/')[-1].split('/')[0]
        zip_filename = f"reddit_{subreddit}_{sort_by}_{post_limit}posts.zip"

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{zip_filename}"'
            }
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    return JSONResponse(content=scraper.progress) 