#!/usr/bin/env python3
"""
Example Usage Scripts for Web Knowledge Aggregator Agent
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Import the aggregator
from aggregator import KnowledgeAggregator
from config import Config

def example_1_basic_usage():
    """Example 1: Basic single topic processing"""
    print("=" * 50)
    print("Example 1: Basic Single Topic Processing")
    print("=" * 50)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    # Process a topic
    topic = "AI in healthcare"
    print(f"Processing topic: {topic}")
    
    try:
        result = aggregator.process_topic(topic)
        
        print(f"✅ Success!")
        print(f"📄 Report saved to: {result['report_path']}")
        print(f"📊 Articles processed: {result['total_articles']}")
        print(f"🔍 Search results found: {result['search_results_count']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_2_custom_settings():
    """Example 2: Custom settings and filename"""
    print("=" * 50)
    print("Example 2: Custom Settings and Filename")
    print("=" * 50)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    # Process with custom settings
    topic = "Climate change solutions"
    max_results = 15
    custom_filename = "climate_solutions_report.md"
    
    print(f"Processing topic: {topic}")
    print(f"Max results: {max_results}")
    print(f"Custom filename: {custom_filename}")
    
    try:
        result = aggregator.process_topic(
            topic=topic,
            max_results=max_results,
            output_filename=custom_filename
        )
        
        print(f"✅ Success!")
        print(f"📄 Report saved to: {result['report_path']}")
        print(f"📊 Articles processed: {result['total_articles']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_3_multiple_topics():
    """Example 3: Processing multiple topics"""
    print("=" * 50)
    print("Example 3: Processing Multiple Topics")
    print("=" * 50)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    # Define topics
    topics = [
        "Future of work",
        "Quantum computing applications",
        "Sustainable energy technologies"
    ]
    
    print(f"Processing {len(topics)} topics:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    try:
        results = aggregator.process_multiple_topics(topics, max_results=8)
        
        print(f"\n✅ Processing completed!")
        print(f"📊 Total topics: {len(results)}")
        
        successful = sum(1 for r in results if r['status'] == 'completed')
        failed = len(results) - successful
        
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        
        # Show individual results
        for result in results:
            if result['status'] == 'completed':
                print(f"\n📄 {result['topic']}")
                print(f"   Report: {result['report_path']}")
                print(f"   Articles: {result['total_articles']}")
            else:
                print(f"\n❌ {result['topic']}: {result.get('error', 'Unknown error')}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def example_4_step_by_step():
    """Example 4: Step-by-step processing"""
    print("=" * 50)
    print("Example 4: Step-by-Step Processing")
    print("=" * 50)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    topic = "Machine learning in finance"
    print(f"Processing topic: {topic}")
    
    try:
        # Step 1: Search
        print("\n🔍 Step 1: Searching...")
        search_results = aggregator.search_topic(topic, max_results=10)
        print(f"   Found {len(search_results)} search results")
        
        # Step 2: Scrape
        print("\n📄 Step 2: Scraping content...")
        scraped_content = aggregator.scrape_content(search_results)
        print(f"   Scraped {len(scraped_content)} articles")
        
        # Step 3: Summarize
        print("\n🤖 Step 3: Summarizing...")
        summary_data = aggregator.summarize_content(topic, scraped_content)
        print(f"   Generated summaries for {len(summary_data['articles'])} articles")
        
        # Step 4: Generate report
        print("\n📝 Step 4: Generating report...")
        report_path = aggregator.generate_report(summary_data)
        print(f"   Report saved to: {report_path}")
        
        print("\n✅ Processing completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_5_data_analysis():
    """Example 5: Analyzing the generated data"""
    print("=" * 50)
    print("Example 5: Data Analysis")
    print("=" * 50)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    topic = "Blockchain technology trends"
    print(f"Processing and analyzing topic: {topic}")
    
    try:
        # Process the topic
        result = aggregator.process_topic(topic)
        summary_data = result['summary_data']
        
        print(f"\n📊 Analysis Results:")
        print(f"   Topic: {summary_data['topic']}")
        print(f"   Total articles: {summary_data['total_articles']}")
        
        # Analyze articles
        if summary_data['articles']:
            print(f"\n📚 Article Analysis:")
            
            # Count by extraction method
            methods = {}
            for article in summary_data['articles']:
                method = article.get('method', 'unknown')
                methods[method] = methods.get(method, 0) + 1
            
            print(f"   Extraction methods:")
            for method, count in methods.items():
                print(f"     {method}: {count} articles")
            
            # Average summary length
            summary_lengths = [len(article['summary']) for article in summary_data['articles']]
            avg_length = sum(summary_lengths) / len(summary_lengths)
            print(f"   Average summary length: {avg_length:.0f} characters")
            
            # Show first few titles
            print(f"\n📄 Article Titles:")
            for i, article in enumerate(summary_data['articles'][:3]):
                print(f"   {i+1}. {article['title']}")
        
        # Show insights preview
        if summary_data.get('final_insights'):
            print(f"\n💡 Key Insights Preview:")
            insights = summary_data['final_insights']
            preview = insights[:200] + "..." if len(insights) > 200 else insights
            print(f"   {preview}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_6_system_status():
    """Example 6: System status and configuration"""
    print("=" * 50)
    print("Example 6: System Status and Configuration")
    print("=" * 50)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    # Get system status
    status = aggregator.get_system_status()
    
    print("🔧 System Configuration:")
    for key, value in status['configuration'].items():
        print(f"   {key}: {value}")
    
    print("\n🤖 Azure OpenAI:")
    for key, value in status['azure_openai'].items():
        print(f"   {key}: {value}")
    
    print("\n🧩 Components:")
    for key, value in status['components'].items():
        print(f"   {key}: {value}")
    
    # Validate configuration
    print("\n🔍 Configuration Validation:")
    if aggregator.validate_config():
        print("   ✅ Configuration is valid")
    else:
        print("   ❌ Configuration has issues")

def example_7_batch_processing():
    """Example 7: Batch processing with different settings"""
    print("=" * 50)
    print("Example 7: Batch Processing with Different Settings")
    print("=" * 50)
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    # Define batch jobs
    batch_jobs = [
        {
            "topic": "Artificial Intelligence ethics",
            "max_results": 12,
            "filename": "ai_ethics_report.md"
        },
        {
            "topic": "Remote work productivity",
            "max_results": 8,
            "filename": "remote_work_report.md"
        },
        {
            "topic": "Electric vehicle adoption",
            "max_results": 15,
            "filename": "ev_adoption_report.md"
        }
    ]
    
    print(f"Processing {len(batch_jobs)} batch jobs:")
    
    results = []
    for i, job in enumerate(batch_jobs, 1):
        print(f"\n📋 Job {i}/{len(batch_jobs)}: {job['topic']}")
        
        try:
            result = aggregator.process_topic(
                topic=job['topic'],
                max_results=job['max_results'],
                output_filename=job['filename']
            )
            
            results.append(result)
            print(f"   ✅ Success: {result['report_path']}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results.append({
                "topic": job['topic'],
                "status": "failed",
                "error": str(e)
            })
    
    # Summary
    successful = sum(1 for r in results if r.get('status') == 'completed')
    print(f"\n📊 Batch Processing Summary:")
    print(f"   Total jobs: {len(batch_jobs)}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {len(batch_jobs) - successful}")

def main():
    """Run all examples"""
    print("🌐 Web Knowledge Aggregator - Example Usage")
    print("=" * 60)
    
    examples = [
        example_1_basic_usage,
        example_2_custom_settings,
        example_3_multiple_topics,
        example_4_step_by_step,
        example_5_data_analysis,
        example_6_system_status,
        example_7_batch_processing
    ]
    
    print(f"\nAvailable examples:")
    for i, example in enumerate(examples, 1):
        doc = example.__doc__
        description = doc.split(':')[1].strip() if doc and ':' in doc else "No description"
        print(f"  {i}. {description}")
    
    print(f"\nSelect an example to run (1-{len(examples)}) or 0 to run all:")
    
    try:
        choice = int(input("Enter your choice: "))
        
        if choice == 0:
            print("\nRunning all examples...")
            for example in examples:
                example()
                print("\n" + "=" * 60 + "\n")
        elif 1 <= choice <= len(examples):
            examples[choice - 1]()
        else:
            print("Invalid choice!")
            
    except ValueError:
        print("Please enter a valid number!")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()