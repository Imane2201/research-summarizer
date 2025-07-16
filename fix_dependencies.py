#!/usr/bin/env python3
"""
Fix script for dependency issues in Web Knowledge Aggregator Agent
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Fix dependency issues"""
    print("🔧 Web Knowledge Aggregator - Dependency Fix")
    print("=" * 50)
    
    # Step 1: Uninstall problematic packages
    print("\n📦 Step 1: Uninstalling problematic packages...")
    
    packages_to_remove = [
        "langchain",
        "langchain-openai", 
        "langchain-community",
        "langchain-core",
        "pydantic",
        "langsmith"
    ]
    
    for package in packages_to_remove:
        run_command(f"pip uninstall -y {package}", f"Uninstalling {package}")
    
    # Step 2: Install working versions
    print("\n📦 Step 2: Installing working versions...")
    
    # Install core packages with working versions
    core_packages = [
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "langchain",
        "langchain-openai",
        "langchain-core"
    ]
    
    for package in core_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"❌ Failed to install {package}")
            return False
    
    # Step 3: Install remaining dependencies
    print("\n📦 Step 3: Installing remaining dependencies...")
    
    if not run_command("pip install -r requirements.txt", "Installing all dependencies"):
        print("❌ Failed to install requirements")
        return False
    
    # Step 4: Test the installation
    print("\n🧪 Step 4: Testing installation...")
    
    try:
        import langchain
        import langchain_openai
        import langchain_core
        import pydantic
        print("✅ All packages imported successfully!")
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    print("\n🎉 Dependency fix completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python test_installation.py")
    print("2. Configure your Azure OpenAI credentials in .env")
    print("3. Start using the Web Knowledge Aggregator!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 