# Scrape Reddit
A lightweight web application for downloading media content from Reddit posts.

## Overview
This FastAPI-based web application allows users to:
1. **Input Reddit URLs**: Enter subreddit URLs and configure sorting/post limits
2. **Download Media**: Automatically scrape images, videos, and GIFs from posts
3. **Export**: Download media files in a convenient ZIP archive

## Tech Stack
- **Backend**: Python with FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Infrastructure**: Docker container
- **Key Libraries**: 
  - FastAPI
  - BeautifulSoup4
  - Requests
  - Jinja2

## Features

### 1. Web Interface
- Clean, responsive design with:
  - Reddit URL input
  - Sorting options (Hot/New/Rising/Top)
  - Post limit selector (5-30 posts)
  - Real-time progress tracking
  - Informative tooltips

### 2. Media Scraping
- Supports multiple media types:
  - Images (jpg, jpeg, png, webp)
  - Videos (mp4, webm)
  - GIFs
- Handles various Reddit content:
  - Direct media links
  - Gallery posts
  - Crossposted content
  - Reddit-hosted media
  - Imgur links

### 3. Progress Tracking
- Real-time updates on:
  - Posts processed
  - Files found
  - Current action
- Visual progress bar
- Error handling and user feedback

## Setup and Deployment

### Prerequisites
- Docker and Docker Compose installed on your machine

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/McDevStudios/Reddit-Media-Scraper.git
   cd Reddit-Media-Scraper
   ```

2. Build and start the container:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Open your browser and navigate to `http://localhost:8000`

### Configuration
- The application runs on port `8000` by default
- Configure the port in `docker-compose.yml` if needed
- Downloads are stored in the `downloads` directory

## Usage
1. Enter a valid Reddit URL (e.g., https://reddit.com/r/subreddit)
2. Select sorting method (Hot, New, Rising, or Top with time period)
3. Choose number of posts to process (5-30)
4. Click "Download Media"
5. Wait for processing and download the ZIP file

## Development

### Project Structure
```
├── app/
│   ├── static/
│   │   └── styles.css          # Application styling
│   │   └── templates/
│   │       └── index.html          # Main application template
│   │   └── main.py                 # FastAPI application entry point
│   │   └── scraper.py              # Reddit scraping implementation
│   ├── docker-compose.yml          # Docker compose configuration
│   ├── Dockerfile                  # Docker container definition
│   ├── requirements.txt            # Python dependencies
│   ├── LICENSE                     # MIT license
│   └── README.md                   # Project documentation
└── roadmap.md                  # Development roadmap
```

The application follows a simple, modular structure:
- `app/`: Contains all application code
  - `static/`: Static assets (CSS)
  - `templates/`: HTML templates
  - `main.py`: FastAPI routes and server setup
  - `scraper.py`: Core Reddit scraping functionality
- Root level configuration files for Docker, dependencies, and documentation

## Extras
- Enhanced styling with CSS frameworks
- Data export/import in CSV format

### Running Locally
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 