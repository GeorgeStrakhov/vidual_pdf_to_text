# Visual Slide to Text Converter

A tool that converts PDF presentations into detailed text descriptions, making them suitable for analysis by Large Language Models (LLMs). It processes each slide individually, extracting all visual information, data points, charts, and text into comprehensive textual descriptions.

Uses openrouter to call the LLM for flexibility.

## Installation

### Prerequisites
1. Install Poppler (required for PDF processing):
```
brew install poppler
```

2. Install Python dependencies:
```
pip install -r requirements.txt
```

3. Set your OpenRouter API key:
```
export OPENROUTER_API_KEY=your_api_key_here
```

## Usage

```
python main.py path/to/slides.pdf
```

# With context
```
python main.py path/to/slides.pdf --context "These slides are about machine learning"
```

# With custom output directory
```
python main.py path/to/slides.pdf --output-dir custom_output
```

# Resume from a specific slide
```
python main.py path/to/slides.pdf --start-slide 5
```

# Optionally convert back into PDF for RAG

With only text, but maintaining slide numbers (so taht an agent can reference correct slides later after RAG ingestion)
```
python create_slides.py output/slides.txt --output presentation.pdf
```