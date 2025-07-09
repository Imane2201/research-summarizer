"""
Setup script for Web Knowledge Aggregator Agent
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split("\n")
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]
else:
    requirements = [
        "langchain>=0.1.0",
        "langchain-openai>=0.0.2",
        "langchain-community>=0.0.10",
        "duckduckgo-search>=4.1.1",
        "newspaper3k>=0.2.8",
        "beautifulsoup4>=4.12.2",
        "requests>=2.31.0",
        "lxml>=4.9.3",
        "python-dotenv>=1.0.0",
        "streamlit>=1.29.0",
        "pydantic>=2.5.0",
        "tiktoken>=0.5.2",
    ]

setup(
    name="web-knowledge-aggregator",
    version="1.0.0",
    description="A Python-powered AI agent that searches the web, scrapes content, and generates comprehensive Markdown reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/web-knowledge-aggregator",
    packages=find_packages(),
    py_modules=[
        "config",
        "search_engine",
        "scraper_engine",
        "summarizer",
        "output_writer",
        "aggregator",
        "main",
        "streamlit_app",
        "example_usage",
    ],
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "ui": [
            "streamlit>=1.29.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="ai, web scraping, knowledge aggregation, langchain, azure openai, summarization, research",
    entry_points={
        "console_scripts": [
            "web-knowledge-aggregator=main:main",
            "wka=main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/web-knowledge-aggregator/issues",
        "Source": "https://github.com/yourusername/web-knowledge-aggregator",
        "Documentation": "https://github.com/yourusername/web-knowledge-aggregator/blob/main/README.md",
    },
)