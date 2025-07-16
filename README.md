# 🌐 Web Knowledge Aggregator Agent

A Python-powered AI agent that searches the web, scrapes content, and generates comprehensive Markdown reports using LangChain and Azure OpenAI.

## 🎯 Project Overview

**Give it a topic → it searches the web (no API key) → scrapes key content → summarizes & organizes findings into a Markdown report.**

### Key Features

- 🔍 **Free Web Search**: Uses DuckDuckGo (no API keys required)
- 📄 **Smart Content Scraping**: newspaper3k + BeautifulSoup fallback
- 🤖 **AI Summarization**: LangChain + Azure OpenAI for intelligent summaries
- 📝 **Beautiful Reports**: Clean, organized Markdown outputs
- 🚀 **Multiple Interfaces**: CLI, Interactive mode, and Python API
- 🔧 **Highly Configurable**: Extensive configuration options

## 🧱 Architecture

```
User Input → Search Engine → Scraper Engine → Summarizer → Report Generator
     ↓              ↓              ↓            ↓              ↓
   Topic      DuckDuckGo    newspaper3k    LangChain     Markdown
                Search      BeautifulSoup   Azure OpenAI     + JSON
```

## 📋 Requirements

- Python 3.8+
- Azure OpenAI API access
- Internet connection for web scraping

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd web-knowledge-aggregator

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure OpenAI credentials
# AZURE_OPENAI_API_KEY=your_key_here
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

### 3. Usage

#### Single Topic Research

```bash
python main.py --topic "AI in healthcare"
```

#### Multiple Topics

```bash
python main.py --topics "AI in education" "Machine learning trends" "Future of work"
```

#### Interactive Mode

```bash
python main.py --interactive
```

#### Custom Options

```bash
python main.py --topic "Climate change solutions" --max-results 15 --output my-report.md
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Required |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | Required |
| `AZURE_OPENAI_API_VERSION` | API version | `2023-12-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Deployment name | `gpt-35-turbo` |

### Application Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `MAX_SEARCH_RESULTS` | Maximum search results | 10 |
| `SCRAPING_TIMEOUT` | Scraping timeout (seconds) | 15 |
| `CHUNK_SIZE` | Text chunk size for summarization | 4000 |
| `MAX_SUMMARY_LENGTH` | Maximum summary length | 500 |

## 📚 Usage Examples

### Command Line Interface

```bash
# Basic usage
python main.py --topic "Artificial Intelligence"

# With custom settings
python main.py --topic "Climate Change" --max-results 20 --verbose

# Multiple topics
python main.py --topics "AI" "Blockchain" "IoT" --max-results 8

# System status
python main.py --status
```

### Python API

```python
from aggregator import KnowledgeAggregator

# Initialize
aggregator = KnowledgeAggregator()

# Process a topic
result = aggregator.process_topic("AI in healthcare", max_results=10)

# Access results
print(f"Report saved to: {result['report_path']}")
print(f"Articles processed: {result['total_articles']}")
```

### Interactive Mode

```bash
python main.py --interactive
```

This starts an interactive session where you can:
- Enter topics one by one
- Specify custom settings for each topic
- See immediate results
- Type 'quit' to exit

## 📄 Output Format

The tool generates two types of output:

### 1. Markdown Report (`topic_timestamp.md`)

```markdown
# 🌐 Web Knowledge Aggregator Report

## Topic: AI in Healthcare

**Generated:** 2024-01-15 14:30:00
**Total Articles Analyzed:** 8
**Processing Status:** Complete

---

## 📋 Table of Contents

1. [AI Tools in Medical Diagnosis](#ai-tools-in-medical-diagnosis)
2. [Machine Learning for Drug Discovery](#machine-learning-for-drug-discovery)
...

---

## 📚 Article Summaries

## 📰 AI Tools in Medical Diagnosis

**Source:** https://example.com/ai-medical-diagnosis
**Authors:** Dr. Jane Smith
**Published:** 2024-01-10
**Extraction Method:** newspaper3k

### Summary
AI tools are revolutionizing medical diagnosis by...

---

## 💡 Final Insights

- AI is significantly improving diagnostic accuracy
- Machine learning models are accelerating drug discovery
- Healthcare professionals need training on AI tools
...

---

## 📊 Report Statistics

- **Articles Successfully Processed:** 8
- **Search Method:** DuckDuckGo (Web + News)
- **Summarization:** Azure OpenAI
- **Report Generated:** 2024-01-15 14:30:00
```

### 2. JSON Backup (`topic_timestamp_backup.json`)

Contains raw data including:
- Original search results
- Scraped content
- Individual summaries
- Processing metadata

## 🧩 Components

### 1. Search Engine (`search_engine.py`)
- Uses DuckDuckGo for web search
- Combines regular web results and news
- No API keys required
- Configurable result limits

### 2. Scraper Engine (`scraper_engine.py`)
- Primary: newspaper3k for article extraction
- Fallback: BeautifulSoup for generic content
- Respectful scraping with delays
- Content validation and filtering

### 3. Summarizer (`summarizer.py`)
- LangChain integration
- Azure OpenAI for text summarization
- Chunking for long content
- Custom prompts for quality summaries

### 4. Output Writer (`output_writer.py`)
- Markdown report generation
- JSON backup creation
- Flexible formatting options
- File naming conventions

### 5. Aggregator (`aggregator.py`)
- Main orchestration logic
- Pipeline management
- Error handling
- Progress tracking

## 🔧 Advanced Usage

### Custom Prompts

You can modify the summarization prompts in `summarizer.py`:

```python
self.summary_prompt = PromptTemplate(
    template="""
    Your custom prompt here...
    
    Article Title: {title}
    Content: {text}
    
    Summary:
    """,
    input_variables=["title", "text"]
)
```

### Integration with Other Tools

```python
from aggregator import KnowledgeAggregator
import json

# Initialize aggregator
aggregator = KnowledgeAggregator()

# Process topic
result = aggregator.process_topic("Your Topic")

# Access structured data
summary_data = result['summary_data']
articles = summary_data['articles']

# Process further or integrate with other systems
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Summary: {article['summary']}")
```

## 🚀 Optional Streamlit UI

For a web interface, run:

```bash
streamlit run streamlit_app.py
```

This provides:
- Web-based topic input
- Real-time processing status
- Interactive report viewing
- Download capabilities

## 📊 Performance Considerations

- **Search Speed**: ~2-5 seconds per topic
- **Scraping Speed**: ~1-3 seconds per article
- **Summarization**: ~5-15 seconds per article (depends on content length)
- **Memory Usage**: ~100-500MB depending on content volume

## 🛠️ Troubleshooting

### Common Issues

1. **Import errors**: Install all dependencies with `pip install -r requirements.txt`
2. **Azure OpenAI errors**: Check your API key and endpoint in `.env`
3. **Scraping failures**: Some sites may block scrapers - this is normal
4. **Slow performance**: Reduce `MAX_SEARCH_RESULTS` in config

### Debugging

Enable verbose logging:

```bash
python main.py --topic "Your Topic" --verbose
```

Check system status:

```bash
python main.py --status
```

## 📈 Future Enhancements

- [ ] PDF export functionality
- [ ] More search engines (Bing, Google)
- [ ] Database storage for results
- [ ] REST API endpoints
- [ ] Docker containerization
- [ ] Multi-language support
- [ ] Custom output templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review existing issues
- Create a new issue with detailed information

## 📚 Dependencies

- **langchain**: LLM framework
- **langchain-openai**: Azure OpenAI integration
- **duckduckgo-search**: Free web search
- **newspaper3k**: Article extraction
- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests
- **python-dotenv**: Environment management
- **streamlit**: Optional web UI

---

*Built with ❤️ using Python, LangChain, and Azure OpenAI*

*Made with ❤️ by Imane LABBASSI*

