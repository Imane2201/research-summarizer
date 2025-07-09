"""
Scraper Engine Module - Extracts content from web pages using newspaper3k and BeautifulSoup
"""
import requests
from newspaper import Article
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
import time
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScraperEngine:
    """Web scraper for extracting article content"""
    
    def __init__(self):
        self.timeout = Config.SCRAPING_TIMEOUT
        self.max_content_length = Config.MAX_CONTENT_LENGTH
        self.min_content_length = Config.MIN_CONTENT_LENGTH
        self.user_agent = Config.USER_AGENT
        
        # Common headers to avoid blocking
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def scrape_with_newspaper(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape content using newspaper3k library
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with title, text, authors, and publish_date
        """
        try:
            logger.info(f"Scraping with newspaper3k: {url}")
            
            article = Article(url)
            article.download()
            article.parse()
            
            # Check if content is substantial
            if len(article.text) < self.min_content_length:
                logger.warning(f"Content too short for {url}")
                return None
                
            # Truncate if too long
            text = article.text
            if len(text) > self.max_content_length:
                text = text[:self.max_content_length] + "..."
                
            return {
                "title": article.title or "No title",
                "text": text,
                "authors": ", ".join(article.authors) if article.authors else "Unknown",
                "publish_date": str(article.publish_date) if article.publish_date else "Unknown",
                "url": url,
                "method": "newspaper3k"
            }
            
        except Exception as e:
            logger.error(f"Newspaper3k failed for {url}: {str(e)}")
            return None
    
    def scrape_with_beautifulsoup(self, url: str) -> Optional[Dict[str, str]]:
        """
        Fallback scraper using BeautifulSoup
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with title, text, and url
        """
        try:
            logger.info(f"Scraping with BeautifulSoup: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title = title.get_text().strip() if title else "No title"
            
            # Extract main content
            content_selectors = [
                'article', 'main', '.content', '.post-content', 
                '.entry-content', '.article-content', '.story-body'
            ]
            
            content = None
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    break
            
            if not content:
                # Fallback to body
                content = soup.find('body')
            
            if content:
                # Extract text
                text = content.get_text(separator=' ', strip=True)
                
                # Clean up extra whitespace
                text = ' '.join(text.split())
                
                # Check length
                if len(text) < self.min_content_length:
                    logger.warning(f"Content too short for {url}")
                    return None
                
                # Truncate if too long
                if len(text) > self.max_content_length:
                    text = text[:self.max_content_length] + "..."
                
                return {
                    "title": title,
                    "text": text,
                    "authors": "Unknown",
                    "publish_date": "Unknown",
                    "url": url,
                    "method": "beautifulsoup"
                }
            
            return None
            
        except Exception as e:
            logger.error(f"BeautifulSoup failed for {url}: {str(e)}")
            return None
    
    def scrape_url(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape a single URL with fallback methods
        
        Args:
            url: URL to scrape
            
        Returns:
            Scraped content or None if failed
        """
        # Try newspaper3k first
        content = self.scrape_with_newspaper(url)
        
        if content is None:
            # Fallback to BeautifulSoup
            content = self.scrape_with_beautifulsoup(url)
        
        if content:
            logger.info(f"Successfully scraped {url} using {content['method']}")
        else:
            logger.warning(f"Failed to scrape {url}")
            
        return content
    
    def scrape_multiple(self, urls: List[str], delay: float = 1.0) -> List[Dict[str, str]]:
        """
        Scrape multiple URLs with delay between requests
        
        Args:
            urls: List of URLs to scrape
            delay: Delay between requests in seconds
            
        Returns:
            List of scraped content
        """
        results = []
        
        for i, url in enumerate(urls):
            logger.info(f"Scraping {i+1}/{len(urls)}: {url}")
            
            content = self.scrape_url(url)
            if content:
                results.append(content)
            
            # Add delay between requests to be respectful
            if i < len(urls) - 1:
                time.sleep(delay)
        
        logger.info(f"Successfully scraped {len(results)} out of {len(urls)} URLs")
        return results