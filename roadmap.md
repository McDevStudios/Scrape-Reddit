# Reddit Media Scraper
A lightweight web application for scraping media content from Reddit posts.

## Overview
A containerized web app that allows users to:
1. **Input Reddit URLs**: Paste subreddit URLs and configure scraping parameters
2. **Download Media**: Automatically download images, videos, GIFs, and links from posts
3. **Export**: Save media to user-specified local directories

## Tech Stack
- **Frontend & Backend**: Python with FastAPI (single service)
- **Infrastructure**: Single Docker container
- **Key Libraries**: 
  - PRAW (Python Reddit API Wrapper)
  - FastAPI
  - Jinja2 (for templating)
  - aiofiles (for async file operations)

## Features

### 1. Web Interface
- Simple HTML form with:
  - Reddit URL input field
  - Sorting options (Top/Hot/New)
  - Post limit selector
  - Export directory path input
  - Submit button
- Real-time feedback on scraping progress

### 2. Scraping Engine
- Utilizes PRAW for Reddit API interaction
- Supports downloading:
  - Images (jpg, png, etc.)
  - Videos
  - GIFs
  - Links (saved as text files)
- Handles rate limiting and API compliance

### 3. File Management
- Creates organized directory structure
- Validates file paths
- Handles duplicate files
- Maintains original filenames when possible

### 4. Containerized Architecture
- **Single Container**:
  - Runs Python FastAPI application
  - Handles both web interface and scraping logic
  - Manages file system operations
  - Maps local storage volume for downloads

---

## Development Phases

### Phase 1: Core Setup
1. **Application Structure**
   - Set up FastAPI application
   - Create basic HTML template
   - Configure Docker container
   - Set up Reddit API authentication

2. **Scraping Logic**
   - Implement PRAW connection
   - Create media detection functions
   - Build download handlers
   - Add sorting and limit functionality

3. **File System Operations**
   - Implement directory creation
   - Add file saving logic
   - Handle path validation
   - Manage file naming conflicts

### Phase 2: Web Interface
- Build simple HTML form
- Add basic CSS styling
- Implement form validation
- Create progress feedback mechanism
- Add error handling and user notifications

### Phase 3: Deployment
- Dockerfile configuration
- Volume mapping for downloads
- Environment variable setup
- Documentation for deployment
- Testing on different platforms

---

## Notes
- Application prioritizes simplicity and efficiency
- Single container architecture reduces complexity
- No database needed as files are stored directly in the file system
- FastAPI provides good performance for both web serving and async operations