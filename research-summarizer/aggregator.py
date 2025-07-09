"""
Aggregator Module - Orchestrates the complete knowledge aggregation pipeline
"""
from typing import Dict, List, Optional, Any
import logging
from search_engine import SearchEngine
from scraper_engine import ScraperEngine
from summarizer import Summarizer
from output_writer import OutputWriter
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeAggregator:
    """Main orchestrator for the Web Knowledge Aggregator Agent"""
    
    def __init__(self):
        """Initialize all components"""
        self.search_engine = SearchEngine()
        self.scraper_engine = ScraperEngine()
        self.summarizer = Summarizer()
        self.output_writer = OutputWriter()
        
        logger.info("Knowledge Aggregator initialized")
    
    def validate_config(self) -> bool:
        """
        Validate that all required configuration is present
        
        Returns:
            True if configuration is valid
        """
        required_configs = [
            Config.AZURE_OPENAI_API_KEY,
            Config.AZURE_OPENAI_ENDPOINT,
        ]
        
        missing_configs = []
        for config in required_configs:
            if not config:
                missing_configs.append(config)
        
        if missing_configs:
            logger.error(f"Missing required configuration: {missing_configs}")
            return False
        
        return True
    
    def search_topic(self, topic: str, max_results: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Search for a topic using the search engine
        
        Args:
            topic: Search topic
            max_results: Maximum number of results
            
        Returns:
            List of search results
        """
        logger.info(f"Starting search for topic: {topic}")
        
        if max_results is None:
            max_results = Config.MAX_SEARCH_RESULTS
        
        # Use combined search (web + news)
        search_results = self.search_engine.search_combined(topic, max_results)
        
        logger.info(f"Search completed: {len(search_results)} results found")
        return search_results
    
    def scrape_content(self, search_results: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Scrape content from search results
        
        Args:
            search_results: List of search results with URLs
            
        Returns:
            List of scraped content
        """
        logger.info("Starting content scraping")
        
        # Extract URLs from search results
        urls = [result['href'] for result in search_results if result.get('href')]
        
        if not urls:
            logger.warning("No URLs found in search results")
            return []
        
        # Scrape content
        scraped_content = self.scraper_engine.scrape_multiple(urls)
        
        logger.info(f"Scraping completed: {len(scraped_content)} articles scraped")
        return scraped_content
    
    def summarize_content(self, topic: str, scraped_content: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Summarize scraped content
        
        Args:
            topic: Original search topic
            scraped_content: List of scraped articles
            
        Returns:
            Summary data with articles and insights
        """
        logger.info("Starting content summarization")
        
        if not scraped_content:
            logger.warning("No content to summarize")
            return {
                "topic": topic,
                "articles": [],
                "final_insights": "No content available for summarization.",
                "total_articles": 0
            }
        
        # Create topic summary
        summary_data = self.summarizer.create_topic_summary(topic, scraped_content)
        
        logger.info(f"Summarization completed: {len(summary_data['articles'])} articles summarized")
        return summary_data
    
    def generate_report(self, summary_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Generate and save the final report
        
        Args:
            summary_data: Summary data from summarization
            filename: Optional custom filename
            
        Returns:
            Path to the saved report
        """
        logger.info("Generating final report")
        
        # Save markdown report
        report_path = self.output_writer.save_report(summary_data, filename)
        
        # Save JSON backup
        json_path = self.output_writer.save_json_backup(summary_data)
        
        logger.info(f"Report generation completed: {report_path}")
        return report_path
    
    def process_topic(self, topic: str, max_results: Optional[int] = None, 
                     output_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete end-to-end processing pipeline
        
        Args:
            topic: Topic to research
            max_results: Maximum number of search results
            output_filename: Optional custom output filename
            
        Returns:
            Processing results with paths and summary
        """
        logger.info(f"Starting end-to-end processing for topic: {topic}")
        
        # Validate configuration
        if not self.validate_config():
            raise ValueError("Invalid configuration - check Azure OpenAI settings")
        
        try:
            # Step 1: Search
            search_results = self.search_topic(topic, max_results)
            
            # Step 2: Scrape
            scraped_content = self.scrape_content(search_results)
            
            # Step 3: Summarize
            summary_data = self.summarize_content(topic, scraped_content)
            
            # Step 4: Generate report
            report_path = self.generate_report(summary_data, output_filename)
            
            # Generate quick summary for console
            quick_summary = self.output_writer.generate_quick_summary(summary_data)
            
            result = {
                "topic": topic,
                "status": "completed",
                "report_path": report_path,
                "total_articles": summary_data['total_articles'],
                "search_results_count": len(search_results),
                "scraped_articles_count": len(scraped_content),
                "quick_summary": quick_summary,
                "summary_data": summary_data
            }
            
            logger.info(f"Processing completed successfully for topic: {topic}")
            return result
            
        except Exception as e:
            logger.error(f"Processing failed for topic '{topic}': {str(e)}")
            raise
    
    def process_multiple_topics(self, topics: List[str], max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Process multiple topics in sequence
        
        Args:
            topics: List of topics to research
            max_results: Maximum number of search results per topic
            
        Returns:
            List of processing results
        """
        logger.info(f"Starting processing for {len(topics)} topics")
        
        results = []
        
        for i, topic in enumerate(topics):
            logger.info(f"Processing topic {i+1}/{len(topics)}: {topic}")
            
            try:
                result = self.process_topic(topic, max_results)
                results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to process topic '{topic}': {str(e)}")
                results.append({
                    "topic": topic,
                    "status": "failed",
                    "error": str(e)
                })
        
        logger.info(f"Multi-topic processing completed: {len(results)} results")
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get system status and configuration
        
        Returns:
            System status information
        """
        return {
            "configuration": {
                "max_search_results": Config.MAX_SEARCH_RESULTS,
                "scraping_timeout": Config.SCRAPING_TIMEOUT,
                "chunk_size": Config.CHUNK_SIZE,
                "max_summary_length": Config.MAX_SUMMARY_LENGTH,
                "output_directory": str(Config.OUTPUT_DIR)
            },
            "azure_openai": {
                "endpoint_configured": bool(Config.AZURE_OPENAI_ENDPOINT),
                "api_key_configured": bool(Config.AZURE_OPENAI_API_KEY),
                "api_version": Config.AZURE_OPENAI_API_VERSION,
                "deployment_name": Config.AZURE_OPENAI_DEPLOYMENT_NAME
            },
            "components": {
                "search_engine": "DuckDuckGo",
                "scraper_engine": "newspaper3k + BeautifulSoup",
                "summarizer": "LangChain + Azure OpenAI",
                "output_writer": "Markdown + JSON"
            }
        }