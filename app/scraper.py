import requests
import json
import io
import os
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlencode
import time
import re
from typing import List, Dict
import logging

class RedditScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.progress = {
            "posts_processed": 0,
            "files_found": 0,
            "current_action": "Initializing..."
        }
        self.SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.webp']
        
    def _create_export_directory(self, export_path):
        """Create export directory if it doesn't exist"""
        Path(export_path).mkdir(parents=True, exist_ok=True)
        
    def _is_valid_reddit_url(self, url):
        """Validate Reddit URL"""
        parsed = urlparse(url)
        return bool(re.match(r'^(?:www\.)?reddit\.com/r/[\w-]+/?', parsed.netloc + parsed.path))
        
    def _get_json_url(self, url: str, sort_by: str, after: str = None) -> str:
        """Convert Reddit URL to JSON endpoint with proper limit"""
        url = url.rstrip('/')
        
        # Handle top sorting with time periods
        if sort_by.startswith('top/'):
            time_period = sort_by.split('/')[1]
            url = f'{url}/top'
            params = {
                'raw_json': 1,
                'limit': 25,  # Reddit's default limit per request
                't': time_period  # time period for top sorting
            }
        else:
            url = f'{url}/{sort_by}'
            params = {
                'raw_json': 1,
                'limit': 25  # Reddit's default limit per request
            }
        
        if after:
            params['after'] = after
            
        query_string = urlencode(params)
        return f'{url}.json?{query_string}'
        
    def _get_media_content(self, url) -> tuple[bytes, str]:
        """Get media content and content type"""
        response = requests.get(url, headers=self.headers, stream=True)
        response.raise_for_status()
        content = response.content
        content_type = response.headers.get('content-type', 'application/octet-stream')
        return content, content_type

    def _extract_media_url(self, post_data):
        """Extract media URL from post data with improved detection and deduplication"""
        media_urls = set()  # Using a set to prevent duplicates
        
        # Debug logging
        self.logger.info(f"Processing post: {post_data.get('title', 'No Title')}")
        
        # 1. Direct image/video/gif URLs
        if 'url' in post_data:
            url = post_data['url']
            # Handle direct media links
            if any(url.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS):
                media_urls.add(url)
                self.logger.info(f"Found direct media URL: {url}")
            # Handle imgur links
            elif 'imgur.com' in url:
                if not url.endswith('.jpg'):
                    url = url + '.jpg'
                media_urls.add(url)
                self.logger.info(f"Found Imgur URL: {url}")
            # Handle i.redd.it links
            elif 'i.redd.it' in url:
                media_urls.add(url)
                self.logger.info(f"Found Reddit image URL: {url}")
            # Handle v.redd.it links
            elif 'v.redd.it' in url and 'media' in post_data:
                if 'reddit_video' in post_data['media']:
                    video_url = post_data['media']['reddit_video']['fallback_url']
                    media_urls.add(video_url)
                    self.logger.info(f"Found Reddit video URL: {video_url}")

        # 2. Gallery posts
        if 'gallery_data' in post_data and 'media_metadata' in post_data:
            self.logger.info("Found gallery post")
            for item in post_data['gallery_data']['items']:
                media_id = item['media_id']
                if media_id in post_data['media_metadata']:
                    metadata = post_data['media_metadata'][media_id]
                    if 's' in metadata:
                        image_url = metadata['s'].get('u', '')
                        if image_url:
                            # Fix URL encoding
                            image_url = image_url.replace('&amp;', '&')
                            media_urls.add(image_url)
                            self.logger.info(f"Found gallery image URL: {image_url}")

        # 3. Crosspost handling
        if 'crosspost_parent_list' in post_data:
            self.logger.info("Found crosspost")
            parent_post = post_data['crosspost_parent_list'][0]
            parent_urls = self._extract_media_url(parent_post)
            if parent_urls:
                media_urls.update(parent_urls)

        # 4. Rich video handling
        if 'media' in post_data and post_data['media']:
            if 'reddit_video' in post_data['media']:
                video_url = post_data['media']['reddit_video']['fallback_url']
                media_urls.add(video_url)
                self.logger.info(f"Found rich video URL: {video_url}")

        if not media_urls:
            self.logger.info("No media found in post")
            
        return list(media_urls) if media_urls else None

    async def scrape(self, reddit_url: str, sort_by: str, post_limit: int) -> List[Dict]:
        """Scrape Reddit posts with strict post limit enforcement"""
        if not self._is_valid_reddit_url(reddit_url):
            raise ValueError("Invalid Reddit URL")

        # Reset progress
        self.progress = {
            "posts_processed": 0,
            "files_found": 0,
            "current_action": "Starting scrape..."
        }

        media_files = []
        after = None
        post_limit = int(post_limit)  # Ensure integer
        posts_processed = 0

        while posts_processed < post_limit:
            try:
                json_url = self._get_json_url(reddit_url, sort_by, after)
                self.progress["current_action"] = f"Fetching posts ({posts_processed}/{post_limit})..."
                
                response = requests.get(json_url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                posts = data['data']['children']
                if not posts:
                    break

                # Calculate remaining posts to process
                remaining = post_limit - posts_processed
                posts_to_process = posts[:remaining]

                for post in posts_to_process:
                    if posts_processed >= post_limit:
                        break
                        
                    post_data = post['data']
                    self.progress["current_action"] = f"Processing post {posts_processed + 1}/{post_limit}"
                    
                    media_urls = self._extract_media_url(post_data)
                    if media_urls:
                        # Only process this post if we found media
                        posts_processed += 1
                        self.progress["posts_processed"] = posts_processed
                        
                        for url in media_urls:
                            try:
                                content, content_type = self._get_media_content(url)
                                filename = f"{post_data['id']}_{media_urls.index(url)}{self._get_extension(url, content_type)}"
                                
                                media_files.append({
                                    'filename': filename,
                                    'content': content,
                                    'content_type': content_type
                                })
                                self.progress["files_found"] += 1
                                
                            except Exception as e:
                                self.logger.error(f"Error downloading {url}: {str(e)}")
                                continue

                if posts_processed >= post_limit:
                    break

                after = data['data'].get('after')
                if not after:
                    break

                time.sleep(1)  # Rate limiting

            except Exception as e:
                self.progress["current_action"] = f"Error: {str(e)}"
                raise

        self.progress["current_action"] = "Download complete!"
        return media_files

    def _get_extension(self, url, content_type=None):
        """Get file extension with improved type detection"""
        # Try to get extension from URL first
        parsed = urlparse(url)
        path = parsed.path
        ext = path.split('.')[-1].lower() if '.' in path else ''
        
        # Validate or get from content type
        valid_extensions = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'video/mp4': '.mp4',
            'video/webm': '.webm'
        }
        
        if content_type in valid_extensions:
            return valid_extensions[content_type]
        elif ext in ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'webm']:
            return f'.{ext}'
        else:
            return '.jpg'  # Default to jpg 