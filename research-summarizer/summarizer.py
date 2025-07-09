"""
Summarizer Module - Uses LangChain with Azure OpenAI for content summarization
"""
from typing import List, Dict, Optional, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Summarizer:
    """Content summarizer using LangChain and Azure OpenAI"""
    
    def __init__(self):
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP
        self.max_summary_length = Config.MAX_SUMMARY_LENGTH
        
        # Initialize Azure OpenAI
        self.llm = AzureOpenAI(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            deployment_name=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.3,
            max_tokens=self.max_summary_length
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        
        # Custom prompts
        self.summary_prompt = PromptTemplate(
            template="""
            Please provide a comprehensive summary of the following article content.
            Focus on key insights, main arguments, and important facts.
            Keep the summary concise but informative.
            
            Article Title: {title}
            URL: {url}
            
            Content:
            {text}
            
            Summary:
            """,
            input_variables=["title", "url", "text"]
        )
        
        self.final_insights_prompt = PromptTemplate(
            template="""
            Based on the following article summaries about "{topic}", provide key insights and conclusions.
            Identify common themes, contradictions, and important takeaways.
            Format as bullet points with clear, actionable insights.
            
            Article Summaries:
            {summaries}
            
            Key Insights:
            """,
            input_variables=["topic", "summaries"]
        )
    
    def summarize_single_article(self, article: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Summarize a single article
        
        Args:
            article: Dictionary containing title, text, url, etc.
            
        Returns:
            Dictionary with original article info plus summary
        """
        try:
            logger.info(f"Summarizing article: {article['title']}")
            
            # Prepare text for summarization
            text = article['text']
            
            # If text is short enough, summarize directly
            if len(text) <= self.chunk_size:
                prompt = self.summary_prompt.format(
                    title=article['title'],
                    url=article['url'],
                    text=text
                )
                
                summary = self.llm(prompt)
                
                return {
                    **article,
                    "summary": summary.strip()
                }
            
            # For longer texts, use chunking
            docs = self.text_splitter.create_documents([text])
            
            # Load summarize chain
            chain = load_summarize_chain(
                self.llm,
                chain_type="map_reduce",
                verbose=False
            )
            
            summary = chain.run(docs)
            
            return {
                **article,
                "summary": summary.strip()
            }
            
        except Exception as e:
            logger.error(f"Summarization failed for {article['title']}: {str(e)}")
            return {
                **article,
                "summary": f"Summary unavailable: {str(e)}"
            }
    
    def summarize_multiple_articles(self, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Summarize multiple articles
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of articles with summaries added
        """
        summarized_articles = []
        
        for i, article in enumerate(articles):
            logger.info(f"Summarizing article {i+1}/{len(articles)}")
            
            summarized_article = self.summarize_single_article(article)
            if summarized_article:
                summarized_articles.append(summarized_article)
        
        logger.info(f"Successfully summarized {len(summarized_articles)} articles")
        return summarized_articles
    
    def generate_final_insights(self, topic: str, summarized_articles: List[Dict[str, str]]) -> str:
        """
        Generate final insights from all summarized articles
        
        Args:
            topic: The search topic
            summarized_articles: List of articles with summaries
            
        Returns:
            Final insights string
        """
        try:
            logger.info("Generating final insights")
            
            # Combine all summaries
            summaries_text = "\n\n".join([
                f"Article: {article['title']}\nSource: {article['url']}\nSummary: {article['summary']}"
                for article in summarized_articles
            ])
            
            # Generate insights
            prompt = self.final_insights_prompt.format(
                topic=topic,
                summaries=summaries_text
            )
            
            insights = self.llm(prompt)
            
            return insights.strip()
            
        except Exception as e:
            logger.error(f"Final insights generation failed: {str(e)}")
            return f"Insights generation failed: {str(e)}"
    
    def create_topic_summary(self, topic: str, articles: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Complete summarization pipeline for a topic
        
        Args:
            topic: The search topic
            articles: List of scraped articles
            
        Returns:
            Dictionary with summarized articles and final insights
        """
        logger.info(f"Starting summarization pipeline for topic: {topic}")
        
        # Summarize individual articles
        summarized_articles = self.summarize_multiple_articles(articles)
        
        # Generate final insights
        final_insights = self.generate_final_insights(topic, summarized_articles)
        
        return {
            "topic": topic,
            "articles": summarized_articles,
            "final_insights": final_insights,
            "total_articles": len(summarized_articles)
        }