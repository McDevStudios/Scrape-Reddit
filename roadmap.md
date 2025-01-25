# Scrape Reddit
A lightweight web application for scraping media content from Reddit posts.

## Overview
A containerized web app that allows users to:
1. **Input Reddit URLs**: Paste subreddit URLs and configure scraping parameters.
2. **Download Media**: Automatically download images, videos, and GIFs from posts.
3. **Export**: Package downloaded media into convenient ZIP archives.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript.
- **Backend**: Python with FastAPI.
- **Infrastructure**: Docker container.
- **Key Libraries**: 
  - FastAPI (web framework).
  - BeautifulSoup4 (HTML parsing).
  - Requests (HTTP client).
  - Jinja2 (templating).

## Features

### 1. Web Interface
- Clean HTML form with:
  - Reddit URL input field.
  - Sorting options (Hot/New/Rising/Top).
  - Post limit selector (5-30 posts).
  - Download button.
  - Info tooltip.
- Real-time progress tracking.
- Responsive design.
- Error handling and feedback.

### 2. Scraping Engine
- Direct Reddit JSON API interaction.
- Supports downloading:
  - Images (jpg, jpeg, png, webp).
  - Videos (mp4, webm).
  - GIFs.
- Handles various content types:
  - Direct media links.
  - Gallery posts.
  - Crossposted content.
  - Reddit-hosted media.
  - Imgur links.
- Built-in rate limiting.

### 3. File Management
- ZIP archive creation.
- Unique filename generation.
- Content-type detection.
- Progress tracking during compression.

### 4. Containerized Architecture
- **Single Container**:
  - FastAPI application server.
  - Static file serving.
  - Media processing.
  - ZIP compression.

---

## Development Phases

### Phase 1: Core Setup ✓
1. **Application Structure**
   - FastAPI application setup.
   - HTML template creation.
   - Docker configuration.
   - Static file serving.

2. **Scraping Logic**
   - Reddit JSON API integration.
   - Media URL extraction.
   - Content type detection.
   - Download handling.

3. **File Operations**
   - ZIP archive creation.
   - Progress tracking.
   - Error handling.
   - Content streaming.

### Phase 2: Web Interface ✓
- Responsive HTML/CSS design.
- Real-time progress updates.
- Form validation.
- Error messaging.
- Loading indicators.
- Info tooltips.

### Phase 3: Deployment ✓
- Docker container configuration.
- Environment setup.
- Port mapping.
- Documentation.
- License.

---

## Notes
- Application prioritizes simplicity and efficiency.
- No authentication required for basic Reddit scraping.
- Uses Reddit's JSON API instead of PRAW for lighter dependencies.
- FastAPI provides both async capabilities and web serving.
- Real-time progress updates via polling.