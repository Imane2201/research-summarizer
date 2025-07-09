# 🚀 Quick Start Guide

Get your Web Knowledge Aggregator up and running in minutes!

## ⚡ Fast Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI
```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Required variables:
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL

### 3. Test Installation
```bash
python test_installation.py
```

### 4. Run Your First Research
```bash
python main.py --topic "AI in healthcare"
```

## 🎯 Common Usage Patterns

### Single Topic Research
```bash
python main.py --topic "Climate change solutions"
```

### Multiple Topics
```bash
python main.py --topics "AI trends" "Blockchain" "IoT" --max-results 8
```

### Custom Output
```bash
python main.py --topic "Future of work" --output my-research.md --max-results 15
```

### Interactive Mode
```bash
python main.py --interactive
```

### Web Interface
```bash
streamlit run streamlit_app.py
```

## 🔧 Using the Makefile

For convenience, use the included Makefile:

```bash
make setup      # Complete setup
make run        # Run example
make ui         # Start web interface
make status     # Check system status
make clean      # Clean output files
make help       # Show all commands
```

## 📊 Expected Output

The tool generates:
- **Markdown Report**: `output/topic_timestamp.md` 
- **JSON Backup**: `output/topic_timestamp_backup.json`
- **Console Summary**: Key insights and statistics

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Azure OpenAI Errors**
   - Check your API key in `.env`
   - Verify endpoint URL format
   - Ensure deployment name is correct

3. **Slow Performance**
   - Reduce `--max-results` parameter
   - Check internet connection
   - Some sites may block scrapers (normal)

### Get System Status
```bash
python main.py --status
```

### Run Tests
```bash
python test_installation.py
```

## 🎨 Customization

### Modify Search Results
Edit `config.py`:
```python
MAX_SEARCH_RESULTS = 20  # Default: 10
```

### Change Output Directory
```python
OUTPUT_DIR = Path("my_reports")  # Default: "output"
```

### Custom Prompts
Edit `summarizer.py` to modify AI prompts.

## 📚 Python API Usage

```python
from aggregator import KnowledgeAggregator

# Initialize
aggregator = KnowledgeAggregator()

# Process a topic
result = aggregator.process_topic("Your research topic")

# Access results
print(f"Report: {result['report_path']}")
print(f"Articles: {result['total_articles']}")
```

## 🌐 Web Interface Features

The Streamlit interface provides:
- Real-time processing status
- Interactive topic input
- Download capabilities
- Report preview
- Configuration display

## 📈 Performance Tips

- **Optimal Results**: 5-15 articles per topic
- **Speed**: Each article takes ~5-10 seconds to process
- **Memory**: ~100-500MB depending on content
- **Rate Limits**: Built-in delays respect website policies

## 🔄 Workflow

1. **Search**: DuckDuckGo finds relevant content
2. **Scrape**: Extract article text (newspaper3k + BeautifulSoup)
3. **Summarize**: AI generates concise summaries
4. **Organize**: Create structured Markdown report
5. **Export**: Save as `.md` file with JSON backup

## 🆘 Need Help?

- Check `README.md` for detailed documentation
- Run `python main.py --help` for CLI options
- Use `python test_installation.py` to diagnose issues
- Review example outputs in the `output/` directory

## 🎯 Next Steps

1. **Try Different Topics**: Test various research areas
2. **Adjust Settings**: Experiment with result counts
3. **Explore API**: Use Python integration
4. **Web Interface**: Try the Streamlit UI
5. **Customize**: Modify prompts and configuration

---

*Ready to aggregate knowledge? Start with `python main.py --topic "Your topic here"`! 🚀*