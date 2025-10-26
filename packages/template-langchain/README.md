<div align="center">

# LangChain - Modern LLM Integration Template

**Production-ready FastAPI with LangChain for LLM workflows**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-purple.svg)](https://python.langchain.com)

</div>

---

## What You'll Build

A modern LangChain-powered FastAPI service with optimized model loading at startup, latest LangChain 0.3.x patterns, smart device configuration, dual endpoints for text generation and question answering, production-ready health checks, and real AI testing.

## Quick Start

```bash
# You're already here! Just run:
make start

# The app will download models on first startup (2-3 minutes)
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

> First startup downloads models (~1-2GB), takes 2-3 minutes depending on internet speed.

## LangChain Features

**Optimized Model Loading**
- Models load once during app startup (not per request)
- Memory efficient with reused tokenizer and model instances
- Automatic GPU/CPU device selection
- Graceful error handling with detailed logging
- Connection pooling for efficient inference

**Modern LangChain Patterns**
- Uses `langchain-huggingface` (not deprecated `langchain-community`)
- Latest LangChain 0.3.x API patterns
- Full Pydantic integration for type safety
- Proper error handling and async support

**Smart Configuration**
- Auto device detection (GPU when available, CPU fallback)
- Environment-based config (`.env_dev` and `.env_prod`)
- Configurable model paths and generation parameters
- Runtime overrides per request

**Dual AI Endpoints**
- Text generation for creative text completion
- Question answering for context-based responses
- Both GET (quick testing) and POST (recommended) endpoints
- Flexible parameter control

**Production Monitoring**
- `/health` endpoint with model status and device info
- Structured logging with proper levels
- Detailed error messages for debugging
- Service status and resource information

**Real AI Testing**
- Integration tests use actual model inference (not mocks)
- Session fixtures for efficient test execution
- Comprehensive endpoint and parameter coverage
- Ensures real-world functionality works

## API Endpoints

### Health & Status
```http
GET /health                 # Service status, model info, device config
```

### Text Generation
```http
# Modern POST endpoint (recommended)
POST /text-generation
{
  "text": "The future of artificial intelligence is",
  "max_new_tokens": 100,
  "temperature": 0.7
}

# Legacy GET endpoint (quick testing)
GET /text-generation?text=What%20is%20AI&max_new_tokens=50
```

### Question Answering
```http
# Modern POST endpoint (recommended)
POST /question-answering
{
  "context": "AI is a field of computer science focused on creating intelligent machines.",
  "question": "What is AI?",
  "max_new_tokens": 50
}

# Legacy GET endpoint (quick testing)
GET /question-answering?context=AI%20is...&question=What%20is%20AI?
```

## Development Commands

| Command      | Description                                  |
| ------------ | -------------------------------------------- |
| `make start` | Run app in development mode with auto-reload |
| `make test`  | Run comprehensive test suite with real AI    |
| `make lint`  | Run code quality checks with Ruff            |

## Configuration

Create `.env_dev` file:
```bash
# Model and device settings
TEXT_GENERATION_MODEL="HuggingFaceTB/SmolLM2-360M-Instruct"
DEVICE="auto"  # auto, cpu, cuda

# Generation parameters
MAX_NEW_TOKENS=100
MAX_LENGTH=150
TEMPERATURE=0.7
RANDOM_SEED=42
```

### Model Options

| Model                      | Size | Use Case                    | Memory |
| -------------------------- | ---- | --------------------------- | ------ |
| `SmolLM2-360M-Instruct`    | 360M | Fast inference, development | ~1GB   |
| `SmolLM2-1.7B-Instruct`    | 1.7B | Better quality, production  | ~3GB   |
| `microsoft/DialoGPT-small` | 345M | Conversational AI           | ~1GB   |

### Hardware Requirements

- **Minimum**: 4GB RAM, CPU-only operation
- **Recommended**: 8GB+ RAM, GPU with 2GB+ VRAM
- **GPU Support**: CUDA (NVIDIA) automatically detected
- **Apple Silicon**: Excellent performance with MPS

## Testing

Tests use actual model inference (not mocks):

```bash
make test
# First run downloads models (takes longer)
# Subsequent runs use cached models
```

## Project Structure

```
langchain/
├── src/
│   └── langchain_app/
│       ├── __init__.py
│       └── main.py      # FastAPI app with LangChain integration
├── tests/
│   ├── test_main.py     # Real AI integration tests
│   └── __init__.py
├── pyproject.toml       # Project configuration (uv)
├── .env_dev             # Environment configuration
├── Makefile             # Development commands
├── .gitignore
└── README.md            # This file
```
