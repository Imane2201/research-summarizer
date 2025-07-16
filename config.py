"""
Configuration settings for Web Knowledge Aggregator Agent
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

# Load environment variables from .env file in the script directory
env_file = SCRIPT_DIR / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ Loaded environment from: {env_file}")
else:
    print(f"⚠️ .env file not found at: {env_file}")
    print("💡 Please create a .env file with your Azure OpenAI credentials")
    print("   Example .env file content:")
    print("   AZURE_OPENAI_API_KEY=your_api_key_here")
    print("   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")

class Config:
    """Application configuration"""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
    
    # Search Configuration
    MAX_SEARCH_RESULTS = 10
    SEARCH_TIMEOUT = 30
    
    # Scraping Configuration
    SCRAPING_TIMEOUT = 15
    MAX_CONTENT_LENGTH = 10000
    MIN_CONTENT_LENGTH = 100
    
    # Summarization Configuration
    CHUNK_SIZE = 4000
    CHUNK_OVERLAP = 200
    MAX_SUMMARY_LENGTH = 500
    
    # Output Configuration
    OUTPUT_DIR = Path("output")
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # User Agent for web scraping
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"