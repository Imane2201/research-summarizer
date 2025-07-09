"""
Search Engine Module - Uses DuckDuckGo for web search (no API key needed)
"""
import asyncio
from typing import List, Dict, Optional
from duckduckgo_search import DDGS
from config import Config
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchEngine:
    """Web search engine using DuckDuckGo"""
    
    def __init__(self):
        self.ddgs = DDGS()
        self.max_results = Config.MAX_SEARCH_RESULTS
        self.timeout = Config.SEARCH_TIMEOUT
    
    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Search for a topic using DuckDuckGo
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, href, and snippet
        """
        if max_results is None:
            max_results = self.max_results
            
        try:
            logger.info(f"Searching for: {query}")
            
            # Perform the search
            results = []
            search_results = self.ddgs.text(
                query,
                region='wt-wt',
                safesearch='moderate',
                timelimit=None,
                max_results=max_results
            )
            time.sleep(2)  # Add delay after search request
            
            for result in search_results:
                formatted_result = {
                    "title": result.get("title", ""),
                    "href": result.get("href", ""),
                    "snippet": result.get("body", "")
                }
                results.append(formatted_result)
                
            logger.info(f"Found {len(results)} search results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def search_news(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Search for news articles using DuckDuckGo News
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of news results with title, href, and snippet
        """
        if max_results is None:
            max_results = self.max_results
            
        try:
            logger.info(f"Searching news for: {query}")
            
            results = []
            news_results = self.ddgs.news(
                query,
                region='wt-wt',
                safesearch='moderate',
                timelimit='m',  # Last month
                max_results=max_results
            )
            time.sleep(2)  # Add delay after news search request
            
            for result in news_results:
                formatted_result = {
                    "title": result.get("title", ""),
                    "href": result.get("url", ""),
                    "snippet": result.get("body", ""),
                    "date": result.get("date", ""),
                    "source": result.get("source", "")
                }
                results.append(formatted_result)
                
            logger.info(f"Found {len(results)} news results")
            return results
            
        except Exception as e:
            logger.error(f"News search error: {str(e)}")
            return []
    
    def search_combined(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Search both regular web results and news
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            Combined list of search results
        """
        if max_results is None:
            max_results = self.max_results
            
        # Split results between web and news
        web_results = max_results // 2
        news_results = max_results - web_results
        
        # Get both types of results
        web_data = self.search(query, web_results)
        time.sleep(2)  # Add delay between web and news search
        news_data = self.search_news(query, news_results)
        
        # Combine and return
        combined_results = web_data + news_data
        logger.info(f"Combined search returned {len(combined_results)} total results")
        
        return combined_results