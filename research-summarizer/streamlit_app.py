"""
Streamlit Web Interface for Web Knowledge Aggregator Agent
"""
import streamlit as st
import json
from datetime import datetime
import os
from pathlib import Path
import time

# Import your components
from aggregator import KnowledgeAggregator
from config import Config

# Page configuration
st.set_page_config(
    page_title="Web Knowledge Aggregator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_configuration():
    """Check if the system is properly configured"""
    if not Config.AZURE_OPENAI_API_KEY:
        return False, "Azure OpenAI API Key is not configured"
    if not Config.AZURE_OPENAI_ENDPOINT:
        return False, "Azure OpenAI Endpoint is not configured"
    return True, "Configuration is valid"

def display_system_status():
    """Display system status in sidebar"""
    st.sidebar.header("🔧 System Status")
    
    # Check configuration
    config_valid, config_message = check_configuration()
    
    if config_valid:
        st.sidebar.success("✅ Configuration Valid")
    else:
        st.sidebar.error(f"❌ {config_message}")
    
    # Display configuration
    st.sidebar.subheader("⚙️ Settings")
    st.sidebar.write(f"**Max Search Results:** {Config.MAX_SEARCH_RESULTS}")
    st.sidebar.write(f"**Scraping Timeout:** {Config.SCRAPING_TIMEOUT}s")
    st.sidebar.write(f"**Chunk Size:** {Config.CHUNK_SIZE}")
    st.sidebar.write(f"**Max Summary Length:** {Config.MAX_SUMMARY_LENGTH}")
    
    # Output directory
    st.sidebar.subheader("📁 Output")
    st.sidebar.write(f"**Directory:** {Config.OUTPUT_DIR}")
    
    # Display recent reports
    display_recent_reports()

def display_recent_reports():
    """Display recent reports in sidebar"""
    st.sidebar.subheader("📄 Recent Reports")
    
    if Config.OUTPUT_DIR.exists():
        # Get recent .md files
        md_files = sorted(
            [f for f in Config.OUTPUT_DIR.glob("*.md")],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )[:5]  # Show last 5 reports
        
        if md_files:
            for file in md_files:
                file_time = datetime.fromtimestamp(file.stat().st_mtime)
                st.sidebar.write(f"📄 {file.name}")
                st.sidebar.caption(f"Generated: {file_time.strftime('%Y-%m-%d %H:%M')}")
        else:
            st.sidebar.info("No reports generated yet")
    else:
        st.sidebar.info("Output directory not found")

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🌐 Web Knowledge Aggregator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">🔍 Search → 📄 Scrape → 🤖 Summarize → 📝 Report</p>', unsafe_allow_html=True)
    
    # Display system status
    display_system_status()
    
    # Check configuration
    config_valid, config_message = check_configuration()
    
    if not config_valid:
        st.markdown(f'<div class="error-box"><strong>Configuration Error:</strong> {config_message}</div>', unsafe_allow_html=True)
        st.info("Please check your .env file and ensure Azure OpenAI credentials are set correctly.")
        return
    
    # Main interface
    st.markdown("---")
    
    # Topic input section
    st.header("📝 Topic Input")
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["Single Topic", "Multiple Topics"])
    
    with tab1:
        single_topic_interface()
    
    with tab2:
        multiple_topic_interface()

def single_topic_interface():
    """Interface for single topic processing"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_input(
            "Enter a topic to research:",
            placeholder="e.g., AI in healthcare, Climate change solutions, Future of work",
            key="single_topic"
        )
    
    with col2:
        max_results = st.number_input(
            "Max Results:",
            min_value=1,
            max_value=50,
            value=Config.MAX_SEARCH_RESULTS,
            key="single_max_results"
        )
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            custom_filename = st.text_input(
                "Custom filename (optional):",
                placeholder="my-report.md",
                key="single_filename"
            )
        
        with col2:
            include_json = st.checkbox(
                "Include JSON backup",
                value=True,
                key="single_json"
            )
    
    # Process button
    if st.button("🚀 Process Topic", key="single_process", type="primary"):
        if not topic:
            st.error("Please enter a topic to research")
            return
        
        process_single_topic(topic, max_results, custom_filename, include_json)

def multiple_topic_interface():
    """Interface for multiple topic processing"""
    st.write("Enter multiple topics (one per line):")
    
    topics_text = st.text_area(
        "Topics:",
        placeholder="AI in healthcare\nClimate change solutions\nFuture of work",
        height=150,
        key="multiple_topics"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_results = st.number_input(
            "Max Results per Topic:",
            min_value=1,
            max_value=50,
            value=Config.MAX_SEARCH_RESULTS,
            key="multiple_max_results"
        )
    
    with col2:
        include_json = st.checkbox(
            "Include JSON backups",
            value=True,
            key="multiple_json"
        )
    
    # Process button
    if st.button("🚀 Process All Topics", key="multiple_process", type="primary"):
        if not topics_text.strip():
            st.error("Please enter at least one topic")
            return
        
        topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()]
        
        if not topics:
            st.error("Please enter valid topics")
            return
        
        process_multiple_topics(topics, max_results, include_json)

def process_single_topic(topic, max_results, custom_filename, include_json):
    """Process a single topic with progress tracking"""
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Search
        status_text.text("🔍 Searching for content...")
        progress_bar.progress(20)
        
        search_results = aggregator.search_topic(topic, max_results)
        
        # Step 2: Scrape
        status_text.text("📄 Scraping articles...")
        progress_bar.progress(40)
        
        scraped_content = aggregator.scrape_content(search_results)
        
        # Step 3: Summarize
        status_text.text("🤖 Generating summaries...")
        progress_bar.progress(70)
        
        summary_data = aggregator.summarize_content(topic, scraped_content)
        
        # Step 4: Generate report
        status_text.text("📝 Generating report...")
        progress_bar.progress(90)
        
        report_path = aggregator.generate_report(summary_data, custom_filename)
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Processing completed!")
        
        # Display results
        display_results(summary_data, report_path, include_json)
        
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        status_text.text("❌ Processing failed")

def process_multiple_topics(topics, max_results, include_json):
    """Process multiple topics with progress tracking"""
    
    # Initialize aggregator
    aggregator = KnowledgeAggregator()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    
    for i, topic in enumerate(topics):
        try:
            status_text.text(f"🔍 Processing topic {i+1}/{len(topics)}: {topic}")
            progress_bar.progress((i * 100) // len(topics))
            
            result = aggregator.process_topic(topic, max_results)
            results.append(result)
            
        except Exception as e:
            st.error(f"Failed to process '{topic}': {str(e)}")
            results.append({
                "topic": topic,
                "status": "failed",
                "error": str(e)
            })
    
    # Complete
    progress_bar.progress(100)
    status_text.text("✅ All topics processed!")
    
    # Display results
    display_multiple_results(results, include_json)

def display_results(summary_data, report_path, include_json):
    """Display results for a single topic"""
    
    st.markdown("---")
    st.header("📊 Results")
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Articles Processed", summary_data['total_articles'])
    
    with col2:
        st.metric("Report Generated", "✅")
    
    with col3:
        st.metric("Status", "Complete")
    
    # Download section
    st.subheader("📥 Download Reports")
    
    # Markdown report
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        st.download_button(
            label="📄 Download Markdown Report",
            data=markdown_content,
            file_name=os.path.basename(report_path),
            mime="text/markdown"
        )
    
    # JSON backup
    if include_json:
        json_data = json.dumps(summary_data, indent=2, ensure_ascii=False)
        st.download_button(
            label="📋 Download JSON Backup",
            data=json_data,
            file_name=f"{summary_data['topic']}_backup.json",
            mime="application/json"
        )
    
    # Preview section
    st.subheader("👁️ Report Preview")
    
    # Show final insights
    if summary_data.get('final_insights'):
        st.markdown("**💡 Key Insights:**")
        st.markdown(summary_data['final_insights'])
    
    # Show article summaries
    if summary_data.get('articles'):
        st.markdown("**📚 Article Summaries:**")
        
        for i, article in enumerate(summary_data['articles'][:3]):  # Show first 3
            with st.expander(f"📰 {article['title']}"):
                st.write(f"**Source:** {article['url']}")
                st.write(f"**Summary:** {article['summary']}")
        
        if len(summary_data['articles']) > 3:
            st.info(f"... and {len(summary_data['articles']) - 3} more articles in the full report")

def display_multiple_results(results, include_json):
    """Display results for multiple topics"""
    
    st.markdown("---")
    st.header("📊 Results Summary")
    
    # Summary statistics
    successful = sum(1 for r in results if r.get('status') == 'completed')
    failed = len(results) - successful
    total_articles = sum(r.get('total_articles', 0) for r in results if r.get('status') == 'completed')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Topics Processed", len(results))
    
    with col2:
        st.metric("Successful", successful)
    
    with col3:
        st.metric("Total Articles", total_articles)
    
    # Individual results
    st.subheader("📋 Individual Results")
    
    for result in results:
        with st.expander(f"📄 {result['topic']}"):
            if result.get('status') == 'completed':
                st.success(f"✅ Report saved to: {result['report_path']}")
                st.write(f"📊 Articles processed: {result['total_articles']}")
                
                # Download button
                if os.path.exists(result['report_path']):
                    with open(result['report_path'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=content,
                        file_name=os.path.basename(result['report_path']),
                        mime="text/markdown",
                        key=f"download_{result['topic']}"
                    )
                
            else:
                st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()