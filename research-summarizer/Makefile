# Makefile for Web Knowledge Aggregator Agent

.PHONY: install test clean help setup run example ui status

# Default target
help:
	@echo "🌐 Web Knowledge Aggregator Agent - Available Commands"
	@echo "=================================================="
	@echo "setup      - Initial setup (create .env, install dependencies)"
	@echo "install    - Install dependencies"
	@echo "test       - Run installation tests"
	@echo "run        - Run example with AI in healthcare topic"
	@echo "example    - Run example usage script"
	@echo "ui         - Start Streamlit web interface"
	@echo "status     - Check system status"
	@echo "clean      - Clean output files and logs"
	@echo "help       - Show this help message"

# Initial setup
setup:
	@echo "🚀 Setting up Web Knowledge Aggregator..."
	@echo "1. Installing dependencies..."
	pip install -r requirements.txt
	@echo "2. Creating .env file..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "✅ .env file created - please configure your Azure OpenAI credentials"; else echo "ℹ️ .env file already exists"; fi
	@echo "3. Creating output directory..."
	@mkdir -p output
	@echo "4. Running installation test..."
	python test_installation.py
	@echo "✅ Setup complete!"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Run tests
test:
	@echo "🧪 Running installation tests..."
	python test_installation.py

# Run example
run:
	@echo "🏃 Running example with 'AI in healthcare' topic..."
	python main.py --topic "AI in healthcare" --max-results 5

# Run example usage script
example:
	@echo "📚 Running example usage script..."
	python example_usage.py

# Start Streamlit UI
ui:
	@echo "🌐 Starting Streamlit web interface..."
	streamlit run streamlit_app.py

# Check system status
status:
	@echo "🔍 Checking system status..."
	python main.py --status

# Clean output files
clean:
	@echo "🧹 Cleaning output files..."
	@rm -rf output/*.md output/*.json
	@rm -f knowledge_aggregator.log
	@rm -rf __pycache__ *.pyc
	@echo "✅ Cleanup complete!"

# Development setup
dev-setup: install
	@echo "🔧 Setting up development environment..."
	pip install black flake8 mypy pytest
	@echo "✅ Development setup complete!"

# Format code
format:
	@echo "🎨 Formatting code..."
	black *.py
	@echo "✅ Code formatted!"

# Lint code
lint:
	@echo "🔍 Linting code..."
	flake8 *.py
	mypy *.py
	@echo "✅ Linting complete!"

# Quick demo
demo:
	@echo "🎯 Running quick demo..."
	@echo "This will process 3 topics with 5 results each:"
	python main.py --topics "AI trends" "Climate tech" "Remote work" --max-results 5

# Interactive mode
interactive:
	@echo "🎮 Starting interactive mode..."
	python main.py --interactive

# Show configuration
config:
	@echo "⚙️ Current configuration:"
	@python -c "from config import Config; import pprint; pprint.pprint({k: v for k, v in Config.__dict__.items() if not k.startswith('_')})"

# Create sample .env for testing
env-sample:
	@echo "📝 Creating sample .env with placeholder values..."
	@echo "AZURE_OPENAI_API_KEY=your_api_key_here" > .env
	@echo "AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/" >> .env
	@echo "AZURE_OPENAI_API_VERSION=2023-12-01-preview" >> .env
	@echo "AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo" >> .env
	@echo "✅ Sample .env created - replace with your actual credentials"

# Show project structure
structure:
	@echo "📁 Project structure:"
	@find . -type f -name "*.py" | head -20
	@echo "..."
	@echo "📊 Files overview:"
	@echo "Python files: $(shell find . -name '*.py' | wc -l)"
	@echo "Total files: $(shell find . -type f | wc -l)"

# Install for development
install-dev:
	@echo "🔧 Installing for development..."
	pip install -e .
	@echo "✅ Development installation complete!"