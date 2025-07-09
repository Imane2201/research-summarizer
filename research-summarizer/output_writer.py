"""
Output Writer Module - Generates clean Markdown reports
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OutputWriter:
    """Generates formatted Markdown reports"""
    
    def __init__(self):
        self.output_dir = Config.OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for safe file system usage
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove or replace problematic characters
        import re
        filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
        filename = re.sub(r'\s+', '-', filename)
        filename = filename.strip('-')
        
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename
    
    def format_article_section(self, article: Dict[str, str]) -> str:
        """
        Format a single article as a Markdown section
        
        Args:
            article: Article dictionary with title, summary, etc.
            
        Returns:
            Formatted Markdown section
        """
        title = article.get('title', 'No title')
        url = article.get('url', '')
        summary = article.get('summary', 'No summary available')
        authors = article.get('authors', 'Unknown')
        publish_date = article.get('publish_date', 'Unknown')
        method = article.get('method', 'Unknown')
        
        section = f"""## 📰 {title}

**Source:** {url}  
**Authors:** {authors}  
**Published:** {publish_date}  
**Extraction Method:** {method}  

### Summary
{summary}

---

"""
        return section
    
    def generate_markdown_report(self, summary_data: Dict[str, Any]) -> str:
        """
        Generate complete Markdown report
        
        Args:
            summary_data: Dictionary with topic, articles, and insights
            
        Returns:
            Complete Markdown report as string
        """
        topic = summary_data['topic']
        articles = summary_data['articles']
        final_insights = summary_data['final_insights']
        total_articles = summary_data['total_articles']
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Header
        report = f"""# 🌐 Web Knowledge Aggregator Report

## Topic: {topic}

**Generated:** {timestamp}  
**Total Articles Analyzed:** {total_articles}  
**Processing Status:** Complete  

---

"""
        
        # Add table of contents
        if articles:
            report += """## 📋 Table of Contents

"""
            for i, article in enumerate(articles, 1):
                title = article.get('title', 'No title')
                report += f"{i}. [{title}](#{self.sanitize_filename(title).lower()})\n"
            
            report += "\n---\n\n"
        
        # Add individual article sections
        if articles:
            report += """## 📚 Article Summaries

"""
            for article in articles:
                report += self.format_article_section(article)
        
        # Add final insights
        report += f"""## 💡 Final Insights

{final_insights}

---

## 📊 Report Statistics

- **Articles Successfully Processed:** {total_articles}
- **Search Method:** DuckDuckGo (Web + News)
- **Summarization:** Azure OpenAI
- **Report Generated:** {timestamp}

---

*This report was generated automatically by the Web Knowledge Aggregator Agent.*
"""
        
        return report
    
    def save_report(self, summary_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save the report to a Markdown file
        
        Args:
            summary_data: Dictionary with topic, articles, and insights
            filename: Optional custom filename
            
        Returns:
            Path to the saved file
        """
        topic = summary_data['topic']
        
        # Generate filename if not provided
        if filename is None:
            sanitized_topic = self.sanitize_filename(topic)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{sanitized_topic}_{timestamp}.md"
        
        # Ensure .md extension
        if not filename.endswith('.md'):
            filename += '.md'
        
        file_path = self.output_dir / filename
        
        # Generate report content
        report_content = self.generate_markdown_report(summary_data)
        
        # Save to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            logger.info(f"Report saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
            raise
    
    def save_json_backup(self, summary_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save a JSON backup of the raw data
        
        Args:
            summary_data: Dictionary with topic, articles, and insights
            filename: Optional custom filename
            
        Returns:
            Path to the saved JSON file
        """
        import json
        
        topic = summary_data['topic']
        
        # Generate filename if not provided
        if filename is None:
            sanitized_topic = self.sanitize_filename(topic)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{sanitized_topic}_{timestamp}_backup.json"
        
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        file_path = self.output_dir / filename
        
        # Save to JSON file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON backup saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save JSON backup: {str(e)}")
            raise
    
    def generate_quick_summary(self, summary_data: Dict[str, Any]) -> str:
        """
        Generate a quick summary for console output
        
        Args:
            summary_data: Dictionary with topic, articles, and insights
            
        Returns:
            Quick summary string
        """
        topic = summary_data['topic']
        total_articles = summary_data['total_articles']
        
        summary = f"""
🌐 Web Knowledge Aggregator - Quick Summary

Topic: {topic}
Articles Processed: {total_articles}

💡 Key Insights:
{summary_data['final_insights']}

Report files saved in: {self.output_dir}
"""
        return summary