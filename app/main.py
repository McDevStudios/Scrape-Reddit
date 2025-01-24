from fastapi import FastAPI, Request, Form
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
        # Get media files
        media_files = await scraper.scrape(reddit_url, sort_by, post_limit)
        
        if not media_files:
            return JSONResponse(
                content={"status": "error", "message": "No media files found"},
                status_code=404
            )

        # Create zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in media_files:
                zip_file.writestr(file['filename'], file['content'])
        
        zip_buffer.seek(0)
        
        # Generate filename from subreddit
        subreddit = reddit_url.split('/r/')[-1].split('/')[0]
        zip_filename = f"reddit_{subreddit}_{sort_by}.zip"

        # Return zip file as download
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{zip_filename}"'
            }
        )

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/status")
async def get_status():
    return JSONResponse(content=scraper.progress) 