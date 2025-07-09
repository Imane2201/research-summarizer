#!/usr/bin/env python3
"""
Test script to verify Web Knowledge Aggregator installation
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        # Test core modules
        import config
        print("✅ config module imported successfully")
        
        import search_engine
        print("✅ search_engine module imported successfully")
        
        import scraper_engine
        print("✅ scraper_engine module imported successfully")
        
        import summarizer
        print("✅ summarizer module imported successfully")
        
        import output_writer
        print("✅ output_writer module imported successfully")
        
        import aggregator
        print("✅ aggregator module imported successfully")
        
        import main
        print("✅ main module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_dependencies():
    """Test that all dependencies are installed"""
    print("\n🔍 Testing dependency imports...")
    
    dependencies = [
        ("langchain", "LangChain framework"),
        ("langchain_openai", "LangChain OpenAI integration"),
        ("duckduckgo_search", "DuckDuckGo search"),
        ("newspaper", "Newspaper3k article extraction"),
        ("bs4", "BeautifulSoup HTML parsing"),
        ("requests", "HTTP requests"),
        ("dotenv", "Environment variable management"),
    ]
    
    failed_imports = []
    
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {module} ({description}) imported successfully")
        except ImportError as e:
            print(f"❌ {module} ({description}) import failed: {e}")
            failed_imports.append(module)
    
    # Test optional dependencies
    optional_deps = [
        ("streamlit", "Streamlit web UI"),
        ("tiktoken", "Token counting"),
    ]
    
    print("\n🔍 Testing optional dependencies...")
    for module, description in optional_deps:
        try:
            __import__(module)
            print(f"✅ {module} ({description}) imported successfully")
        except ImportError:
            print(f"⚠️ {module} ({description}) not installed (optional)")
    
    return len(failed_imports) == 0

def test_configuration():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import Config
        
        # Test configuration attributes
        config_attrs = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "MAX_SEARCH_RESULTS",
            "OUTPUT_DIR",
        ]
        
        for attr in config_attrs:
            if hasattr(Config, attr):
                print(f"✅ Configuration attribute {attr} exists")
            else:
                print(f"❌ Configuration attribute {attr} missing")
                return False
        
        # Test output directory creation
        if Config.OUTPUT_DIR.exists():
            print(f"✅ Output directory created: {Config.OUTPUT_DIR}")
        else:
            print(f"❌ Output directory not created: {Config.OUTPUT_DIR}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without requiring Azure OpenAI"""
    print("\n🔍 Testing basic functionality...")
    
    try:
        # Test search engine
        from search_engine import SearchEngine
        search_engine = SearchEngine()
        print("✅ SearchEngine initialized successfully")
        
        # Test scraper engine
        from scraper_engine import ScraperEngine
        scraper_engine = ScraperEngine()
        print("✅ ScraperEngine initialized successfully")
        
        # Test output writer
        from output_writer import OutputWriter
        output_writer = OutputWriter()
        print("✅ OutputWriter initialized successfully")
        
        # Test aggregator (without Azure OpenAI)
        from aggregator import KnowledgeAggregator
        aggregator = KnowledgeAggregator()
        print("✅ KnowledgeAggregator initialized successfully")
        
        # Test system status
        status = aggregator.get_system_status()
        if isinstance(status, dict):
            print("✅ System status retrieved successfully")
        else:
            print("❌ System status not retrieved properly")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_environment_setup():
    """Test environment setup"""
    print("\n🔍 Testing environment setup...")
    
    # Check for .env file
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file exists")
    else:
        print("⚠️ .env file not found")
        if env_example.exists():
            print("💡 .env.example file found - copy it to .env and configure")
        else:
            print("❌ .env.example file not found")
            return False
    
    # Check output directory
    output_dir = Path("output")
    if output_dir.exists():
        print("✅ Output directory exists")
    else:
        print("ℹ️ Output directory will be created automatically")
    
    return True

def test_cli_interface():
    """Test CLI interface"""
    print("\n🔍 Testing CLI interface...")
    
    try:
        import subprocess
        
        # Test help command
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ CLI help command works")
        else:
            print(f"❌ CLI help command failed: {result.stderr}")
            return False
        
        # Test status command
        result = subprocess.run(
            [sys.executable, "main.py", "--status"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ CLI status command works")
        else:
            print(f"⚠️ CLI status command failed (might be due to missing Azure OpenAI config): {result.stderr}")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ CLI test timed out")
        return False
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🌐 Web Knowledge Aggregator - Installation Test")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration),
        ("Basic Functionality", test_basic_functionality),
        ("Environment Setup", test_environment_setup),
        ("CLI Interface", test_cli_interface),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! The Web Knowledge Aggregator is ready to use.")
        print("\n📋 Next steps:")
        print("1. Configure your Azure OpenAI credentials in .env")
        print("2. Run: python main.py --topic 'Your research topic'")
        print("3. Or try the web UI: streamlit run streamlit_app.py")
        return 0
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please check the installation.")
        print("\n🔧 Troubleshooting:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Check your Python version (requires 3.8+)")
        print("3. Verify all files are in the correct location")
        return 1

if __name__ == "__main__":
    sys.exit(main())