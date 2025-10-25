<div align="center">

# NLP - Comprehensive AI Language Processing Template

**Production-ready FastAPI with 8 NLP capabilities using modern Transformers**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.0+-orange.svg)](https://huggingface.co/transformers)

</div>

---

## What You'll Build

A comprehensive NLP service with 8 powerful AI capabilities: text summarization, named entity recognition, text generation, question answering, sentence embeddings, sentiment analysis, zero-shot classification, and text similarity. Production architecture with startup model loading, device auto-detection, model caching, and real AI testing.

## Quick Start

```bash
# Initialize environment:
make init

# Start the app:
make start

# Models download on first startup (2-4 minutes)
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

> First startup downloads models (~1-2GB total), takes 3-5 minutes depending on internet speed.

## 8 NLP Capabilities

**Text Summarization** - Extractive and abstractive summarization with T5-small, configurable length control

**Named Entity Recognition** - Extract persons, organizations, locations with confidence scores and position tracking

**Text Generation** - Creative text completion with SmolLM, temperature control, reproducible output

**Question Answering** - Context-based extractive QA with DistilBERT, confidence scores and position tracking

**Sentence Embeddings** - Dense vector representations with MiniLM, perfect for semantic search and clustering

**Sentiment Analysis** - Binary positive/negative classification with confidence scores using DistilBERT

**Zero-shot Classification** - Classify into arbitrary custom categories without training data

**Text Similarity** - Calculate semantic similarity between texts with scores from 0 to 1

## API Endpoints

### Health & Status
```http
GET /health                 # Service status, device info, model status
```

### Text Processing
```http
POST /summarize             # Text summarization
POST /ner                   # Named entity recognition
POST /text-generation       # Text generation
POST /question-answering    # Question answering
```

### Advanced Analysis
```http
POST /embeddings            # Sentence embeddings
POST /sentiment             # Sentiment analysis
POST /classify              # Zero-shot classification
POST /similarity            # Text similarity
```

## Development Commands

| Command      | Description                                        |
| ------------ | -------------------------------------------------- |
| `make init`  | Set up Python environment and install dependencies |
| `make start` | Run app in development mode with auto-reload       |
| `make test`  | Run comprehensive test suite with real AI          |
| `make lint`  | Run code quality checks with Ruff                  |

## Configuration

Create `.env_dev` file:
```bash
# Model configurations
SUMMARIZE_MODEL="t5-small"
NER_MODEL="dslim/bert-base-NER"
TEXT_GENERATION_MODEL="HuggingFaceTB/SmolLM-135M"
QA_MODEL="distilbert/distilbert-base-cased-distilled-squad"
EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
SENTIMENT_MODEL="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
ZERO_SHOT_MODEL="typeform/distilbert-base-uncased-mnli"

# Device and performance
DEVICE="auto"  # auto, cpu, cuda, mps
MAX_LENGTH=512
TEMPERATURE=0.7
```

### Alternative Models

**Summarization**: `t5-small` (240MB, fast) | `facebook/bart-large-cnn` (1.6GB, excellent for news) | `google/pegasus-xsum` (2.3GB, academic)

**NER**: `dslim/bert-base-NER` (400MB, high accuracy) | `dslim/bert-large-NER` (1.3GB, higher accuracy)

**Text Generation**: `SmolLM-135M` (270MB, very fast) | `openai-community/gpt2` (500MB, better) | `microsoft/DialoGPT-small` (345MB, conversational)

### Hardware Requirements

- **Minimum**: 8GB RAM, CPU-only operation
- **Recommended**: 16GB+ RAM, GPU with 4GB+ VRAM
- **GPU Support**: CUDA (NVIDIA), MPS (Apple Silicon), CPU fallback

## Production Architecture

**Smart Model Loading**
- All models load during app startup (not on first request)
- Automatic GPU/CPU/MPS detection and utilization
- Models stay in memory for application lifetime
- Single model instances handle multiple concurrent requests
- Graceful error recovery for failed model loads

**Performance Characteristics**
- Cold start: 30-60s (model download and loading)
- Warm inference: <1s for most operations
- GPU acceleration: <500ms when available
- Concurrent requests use shared models

## Testing

Tests use actual model inference (not mocks):

```bash
make test
# First run downloads models (takes longer)
# Subsequent runs use cached models
```

## Project Structure

```
nlp/
├── src/
│   └── nlp/
│       ├── __init__.py
│       └── main.py      # FastAPI app with 8 NLP capabilities
├── tests/
│   ├── test_main.py     # Real AI integration tests
│   └── __init__.py
├── pyproject.toml       # Project configuration (uv)
├── .env_dev             # Environment configuration
├── Makefile             # Development commands
├── .gitignore
└── README.md            # This file
```
