#!/usr/bin/env python3
"""
Web Knowledge Aggregator Agent - Main Entry Point
"""
import argparse
import sys
import json
from pathlib import Path
from typing import List, Optional
import logging

from aggregator import KnowledgeAggregator
from config import Config

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('knowledge_aggregator.log')
        ]
    )

def print_banner():
    """Print application banner"""
    banner = """
Web Knowledge Aggregator Agent
==================================
Search -> Scrape -> Summarize -> Report
"""
    print(banner)

def validate_environment():
    """Validate environment variables"""
    if not Config.AZURE_OPENAI_API_KEY:
        print("❌ Error: AZURE_OPENAI_API_KEY environment variable is required")
        print("💡 Please set it in your .env file or environment")
        return False
    
    if not Config.AZURE_OPENAI_ENDPOINT:
        print("❌ Error: AZURE_OPENAI_ENDPOINT environment variable is required")
        print("💡 Please set it in your .env file or environment")
        return False
    
    return True

def process_single_topic(topic: str, max_results: Optional[int] = None, 
                        output_filename: Optional[str] = None, verbose: bool = False):
    """Process a single topic"""
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    print_banner()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    try:
        print(f"🔍 Processing topic: {topic}")
        print(f"📊 Max results: {max_results or Config.MAX_SEARCH_RESULTS}")
        print("=" * 50)
        
        # Process the topic
        result = aggregator.process_topic(topic, max_results, output_filename)
        
        # Print results
        print("\n✅ Processing completed successfully!")
        print(f"📄 Report saved to: {result['report_path']}")
        print(f"📊 Articles processed: {result['total_articles']}")
        print(f"🔍 Search results: {result['search_results_count']}")
        print(f"📝 Scraped articles: {result['scraped_articles_count']}")
        
        # Print quick summary
        print("\n" + "=" * 50)
        print(result['quick_summary'])
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

def process_multiple_topics(topics: List[str], max_results: Optional[int] = None, 
                           verbose: bool = False):
    """Process multiple topics"""
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    print_banner()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    try:
        print(f"🔍 Processing {len(topics)} topics")
        print(f"📊 Max results per topic: {max_results or Config.MAX_SEARCH_RESULTS}")
        print("=" * 50)
        
        # Process topics
        results = aggregator.process_multiple_topics(topics, max_results)
        
        # Print summary
        successful = sum(1 for r in results if r['status'] == 'completed')
        failed = len(results) - successful
        
        print("\n✅ Multi-topic processing completed!")
        print(f"📊 Topics processed: {len(topics)}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        
        # Print individual results
        for result in results:
            if result['status'] == 'completed':
                print(f"\n📄 {result['topic']}: {result['report_path']}")
            else:
                print(f"\n❌ {result['topic']}: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        logger.error(f"Multi-topic processing failed: {str(e)}")
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

def show_system_status():
    """Show system status and configuration"""
    print_banner()
    
    aggregator = KnowledgeAggregator()
    status = aggregator.get_system_status()
    
    print("🔧 System Status")
    print("=" * 50)
    
    # Configuration
    print("\n📋 Configuration:")
    for key, value in status['configuration'].items():
        print(f"  {key}: {value}")
    
    # Azure OpenAI
    print("\n🤖 Azure OpenAI:")
    for key, value in status['azure_openai'].items():
        print(f"  {key}: {value}")
    
    # Components
    print("\n🧩 Components:")
    for key, value in status['components'].items():
        print(f"  {key}: {value}")
    
    # Environment validation
    print("\n🔍 Environment Validation:")
    if validate_environment():
        print("  ✅ All required environment variables are set")
    else:
        print("  ❌ Missing required environment variables")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Web Knowledge Aggregator Agent - Search, scrape, and summarize web content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "AI in healthcare"
  python main.py --topic "Climate change solutions" --max-results 15
  python main.py --topics "AI in education" "Machine learning trends" "Future of work"
  python main.py --status
  python main.py --interactive
        """
    )
    
    # Main arguments
    parser.add_argument(
        "--topic",
        type=str,
        help="Single topic to research"
    )
    
    parser.add_argument(
        "--topics",
        type=str,
        nargs="+",
        help="Multiple topics to research"
    )
    
    parser.add_argument(
        "--max-results",
        type=int,
        help=f"Maximum number of search results (default: {Config.MAX_SEARCH_RESULTS})"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Custom output filename"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show system status and configuration"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    # Handle different modes
    if args.status:
        show_system_status()
    elif args.interactive:
        run_interactive_mode()
    elif args.topic:
        process_single_topic(args.topic, args.max_results, args.output, args.verbose)
    elif args.topics:
        process_multiple_topics(args.topics, args.max_results, args.verbose)
    else:
        parser.print_help()

def run_interactive_mode():
    """Run in interactive mode"""
    print_banner()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    print("🚀 Interactive Mode - Enter topics to research (type 'quit' to exit)")
    print("=" * 50)
    
    aggregator = KnowledgeAggregator()
    
    while True:
        try:
            topic = input("\n🔍 Enter topic to research: ").strip()
            
            if topic.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not topic:
                print("Please enter a valid topic.")
                continue
            
            # Ask for max results
            max_results_input = input(f"📊 Max results (default {Config.MAX_SEARCH_RESULTS}): ").strip()
            max_results = int(max_results_input) if max_results_input else None
            
            # Process the topic
            print(f"\n🔍 Processing: {topic}")
            print("-" * 30)
            
            result = aggregator.process_topic(topic, max_results)
            
            print(f"\n✅ Completed! Report saved to: {result['report_path']}")
            print(f"📊 Articles processed: {result['total_articles']}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()