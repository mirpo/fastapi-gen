<div align="center">

# NLP - Comprehensive AI Language Processing Template

**Production-ready FastAPI with 8 NLP capabilities using modern Transformers**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.0+-orange.svg)](https://huggingface.co/transformers)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org)

</div>

---

## What You'll Build

A **comprehensive NLP service** with 8 powerful AI capabilities:

**8 NLP Capabilities** → Complete text processing pipeline  
**Production Architecture** → Startup model loading, device auto-detection  
**Smart Configuration** → Environment-based config, multiple models  
**Performance Optimized** → Model caching, concurrent handling, hardware acceleration  
**Production Monitoring** → Health checks, model status, logging  
**Real AI Testing** → Actual model inference validation  

## Quick Start in 30 Seconds

```bash
# You're already here! Initialize the environment:
make init  # Sets up Python environment and dependencies

# Start the app:
make start

# The app will download models on first startup (be patient!)
# Open: http://localhost:8000/docs
```

**Open:** [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

> **First startup:** Downloads models (~1-2GB total), takes 3-5 minutes depending on internet speed.

## 8 NLP Capabilities

<details>
<summary><strong>Text Summarization</strong></summary>

**Advanced text summarization using T5-small:**
- ✅ **Extractive & Abstractive** - Generate concise summaries from long text
- ✅ **Configurable Length** - Control summary length with max_length parameter
- ✅ **Quality Models** - T5-small for balanced speed and quality
- ✅ **Batch Processing** - Handle multiple texts efficiently

**Try it:**
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your long text here...", "max_length": 150}'
```

</details>

<details>
<summary><strong>Named Entity Recognition (NER)</strong></summary>

**Extract entities from text:**
- ✅ **Entity Types** - Persons, organizations, locations, and more
- ✅ **Confidence Scores** - Get confidence levels for each entity
- ✅ **Position Tracking** - Know where entities appear in text
- ✅ **Multiple Models** - Choose between speed and accuracy

**Extracted Entities:**
- PER (Person names)
- ORG (Organizations)
- LOC (Locations)
- MISC (Miscellaneous entities)

</details>

<details>
<summary><strong>Text Generation</strong></summary>

**Creative text generation with SmolLM:**
- ✅ **Prompt Completion** - Continue text from given prompts
- ✅ **Parameter Control** - Temperature, max tokens, and more
- ✅ **Efficient Models** - SmolLM for fast generation
- ✅ **Reproducible Output** - Seed control for consistent results

**Generation Controls:**
- Temperature (creativity level)
- Max new tokens (length control)
- Top-p sampling for quality

</details>

<details>
<summary><strong>Question Answering</strong></summary>

**Context-based question answering:**
- ✅ **Extractive QA** - Find answers within provided context
- ✅ **Confidence Scores** - Get answer confidence levels
- ✅ **Position Tracking** - Know where answers are found
- ✅ **DistilBERT Model** - Fast and accurate processing

**Perfect for:**
- Document question answering
- Knowledge base queries
- FAQ automation

</details>

<details>
<summary><strong>Sentence Embeddings</strong></summary>

**Generate dense vector representations:**
- ✅ **Semantic Vectors** - Convert text to numerical representations
- ✅ **Batch Processing** - Handle multiple texts in one request
- ✅ **MiniLM Model** - Optimized for speed and quality
- ✅ **Similarity Ready** - Perfect for semantic search and clustering

**Use Cases:**
- Semantic search
- Document clustering
- Recommendation systems
- Content similarity

</details>

<details>
<summary><strong>Sentiment Analysis</strong></summary>

**Classify text sentiment:**
- ✅ **Binary Classification** - Positive/Negative sentiment
- ✅ **Confidence Scores** - Numerical confidence levels
- ✅ **Fast Processing** - DistilBERT for speed
- ✅ **Production Ready** - Handles various text types

**Applications:**
- Customer feedback analysis
- Social media monitoring
- Product reviews
- Content moderation

</details>

<details>
<summary><strong>Zero-shot Classification</strong></summary>

**Classify text without training data:**
- ✅ **Custom Categories** - Define your own classification labels
- ✅ **No Training Required** - Classify into arbitrary categories
- ✅ **Ranked Results** - Get probability scores for all labels
- ✅ **Flexible Input** - Any text, any categories

**Example Use Cases:**
- Content categorization
- Intent classification
- Topic modeling
- Dynamic labeling

</details>

<details>
<summary><strong>Text Similarity</strong></summary>

**Calculate semantic similarity between texts:**
- ✅ **Similarity Scores** - Numerical similarity from 0 to 1
- ✅ **Semantic Understanding** - Beyond keyword matching
- ✅ **Fast Computation** - Optimized embeddings
- ✅ **Pairwise Comparison** - Compare any two texts

**Perfect for:**
- Duplicate detection
- Content matching
- Recommendation systems
- Search ranking

</details>

## API Endpoints

### Health & Status
```http
GET /health                 # Service status, device info, model loading status
```

### Text Processing
```http
# Text Summarization
POST /summarize
{
  "text": "Long text to summarize...",
  "max_length": 150
}

# Named Entity Recognition  
POST /ner
{
  "text": "John Smith works at Microsoft in Seattle."
}

# Text Generation
POST /text-generation
{
  "text": "The future of AI is",
  "max_new_tokens": 100,
  "temperature": 0.7
}

# Question Answering
POST /question-answering
{
  "context": "AI is a field of computer science...",
  "question": "What is AI?"
}
```

### Advanced Analysis
```http
# Sentence Embeddings
POST /embeddings
{
  "texts": ["Hello world", "How are you?"]
}

# Sentiment Analysis
POST /sentiment
{
  "text": "I love this product!"
}

# Zero-shot Classification
POST /classify
{
  "text": "I love programming in Python",
  "candidate_labels": ["technology", "sports", "cooking"]
}

# Text Similarity
POST /similarity
{
  "text1": "The cat is sleeping",
  "text2": "A cat is taking a nap"
}
```

## Development Commands

<details>
<summary><strong>Available Make Commands</strong></summary>

| Command | Description |
|---------|-------------|
| `make init` | Set up Python environment and install dependencies |
| `make start` | Run app in development mode with auto-reload |
| `make test` | Run comprehensive test suite with real AI |
| `make lint` | Run code quality checks with Ruff |

</details>

## Configuration & Setup

### Environment Configuration

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

# Device and performance settings
DEVICE="auto"  # auto, cpu, cuda, mps
MAX_LENGTH=512
TEMPERATURE=0.7
TOP_P=0.9
```

### Model Options & Alternatives

<details>
<summary><strong>📝 Summarization Models</strong></summary>

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `t5-small` (default) | 240MB | Fast | Good | Development, balanced |
| `facebook/bart-large-cnn` | 1.6GB | Slower | Excellent | Production, news |
| `google/pegasus-xsum` | 2.3GB | Slowest | Excellent | Academic papers |

</details>

<details>
<summary><strong>🏷️ NER Models</strong></summary>

| Model | Size | Language | Accuracy |
|-------|------|----------|----------|
| `dslim/bert-base-NER` (default) | 400MB | English | High |
| `dslim/bert-large-NER` | 1.3GB | English | Higher |
| `dbmdz/bert-large-cased-finetuned-conll03-english` | 1.3GB | English | Very High |

</details>

<details>
<summary><strong>✍️ Text Generation Models</strong></summary>

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `SmolLM-135M` (default) | 270MB | Very Fast | Good |
| `openai-community/gpt2` | 500MB | Fast | Better |
| `microsoft/DialoGPT-small` | 345MB | Fast | Conversational |

</details>

### Hardware Requirements

- **Minimum:** 8GB RAM, CPU-only operation
- **Recommended:** 16GB+ RAM, GPU with 4GB+ VRAM
- **GPU Support:** 
  - CUDA (NVIDIA) automatically detected
  - MPS (Apple Silicon) excellent performance
  - CPU fallback always available

## Production Architecture

### Smart Model Loading

**Optimized startup patterns:**
- ✅ **Startup Loading** - All models load during app startup (not on first request)
- ✅ **Device Detection** - Automatic GPU/CPU/MPS detection and utilization
- ✅ **Memory Management** - Models stay in memory for application lifetime
- ✅ **Concurrent Handling** - Single model instances handle multiple requests
- ✅ **Error Recovery** - Graceful handling of model loading failures

### Performance Characteristics

| Phase | Duration | Memory Usage | Notes |
|-------|----------|--------------|-------|
| **Cold Start** | 30-60s | ~2-4GB | Model download and loading |
| **Warm Inference** | <1s | ~2-4GB | Most operations under 1 second |
| **GPU Acceleration** | <500ms | 2-6GB VRAM | When available |
| **Concurrent Requests** | Parallel | Shared | Multiple requests use same models |

## Testing Philosophy

**Real AI validation approach:**

```bash
make test
# Tests use actual model inference (not mocks)
# Automatically uses CPU in CI environments
# First run downloads models (takes longer)
# Subsequent runs are fast (cached models)
```

**Comprehensive test coverage:**
- ✅ **Model Loading** - Validates all 8 models load correctly
- ✅ **Inference Testing** - Tests actual AI capabilities
- ✅ **Cross-platform** - CPU/GPU/MPS compatibility
- ✅ **Error Handling** - Invalid inputs and edge cases
- ✅ **Performance** - Response times and memory usage
- ✅ **API Contracts** - Request/response validation

### CI/CD Integration

**GitHub Actions ready:**
```yaml
env:
  CI: true          # Automatically detected
  DEVICE: cpu       # Forces CPU usage in CI
```

The service automatically detects CI environments and switches to CPU mode to avoid memory issues.

## Project Structure

```
nlp/
├── main.py              # FastAPI app with 8 NLP capabilities
├── tests/
│   ├── test_main.py     # Real AI integration tests
│   ├── conftest.py      # Test configuration and fixtures
│   └── __init__.py
├── requirements.txt     # Dependencies (transformers, torch, etc.)
├── .env_dev            # Environment configuration
├── Makefile            # Development commands
└── README.md           # This file
```

## NLP Learning Path

### Mastering AI Text Processing

1. **Setup & Configuration**
   - Run `make init` to set up environment
   - Check `/health` endpoint for model status
   - Experiment with different models in configuration

2. **Text Processing Basics**
   - Try text summarization with different lengths
   - Extract entities from various text types
   - Generate text with different creativity levels

3. **Advanced Analysis**
   - Test question answering with different contexts
   - Analyze sentiment of various text samples
   - Create embeddings for semantic search

4. **Classification & Similarity**
   - Use zero-shot classification for custom categories
   - Calculate text similarity for content matching
   - Combine multiple capabilities for complex workflows

5. **Performance Optimization**
   - Monitor memory usage across models
   - Test GPU vs CPU performance
   - Optimize batch processing for efficiency

6. **Real Testing**
   - Run `make test` to see AI validation
   - Study test patterns for production usage
   - Understand model loading and inference strategies

## Production Deployment

### Security Best Practices

- [ ] Implement API key authentication for all endpoints
- [ ] Add rate limiting based on model complexity
- [ ] Validate and sanitize all text inputs
- [ ] Set up comprehensive request/response logging
- [ ] Configure CORS for specific domains
- [ ] Monitor model usage and associated costs

### Performance Optimization

- [ ] Choose optimal models for your use case (speed vs quality)
- [ ] Use GPU acceleration when available
- [ ] Implement request batching for similar operations
- [ ] Add intelligent caching for frequent requests
- [ ] Monitor memory usage and optimize model selection
- [ ] Consider model quantization for production speed

### Scaling Considerations

- [ ] Set up horizontal scaling with multiple instances
- [ ] Implement load balancing across model servers
- [ ] Configure monitoring for all 8 NLP capabilities
- [ ] Plan for model updates and versioning
- [ ] Set up backup inference endpoints
- [ ] Integrate with model monitoring and analytics tools

## Extension Ideas

<details>
<summary><strong>Advanced NLP Features</strong></summary>

**Ready to implement:**
- Multi-language support with language detection
- Custom fine-tuned models for domain-specific tasks
- Document processing with OCR integration
- Speech-to-text and text-to-speech capabilities
- Advanced prompt engineering and templates

</details>

<details>
<summary><strong>Search & Retrieval</strong></summary>

**AI-powered search features:**
- Vector database integration (Pinecone, Weaviate)
- Semantic search with embeddings
- Retrieval Augmented Generation (RAG)
- Document indexing and search
- Similarity-based recommendation systems

</details>

<details>
<summary><strong>Analytics & Insights</strong></summary>

**Business intelligence features:**
- Text analytics dashboards
- Trend analysis and topic modeling
- Automated content categorization
- Sentiment tracking over time
- Custom classification for business domains

</details>

## Next Steps

### Explore Other AI Templates

- **LLM Integration** - Try the [LangChain template](../langchain/README.md) for conversational AI
- **Local LLM** - Check out [Llama template](../llama/README.md) for local inference
- **Enterprise Features** - Add auth with [Advanced template](../advanced/README.md)

### Learn More About NLP
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [NLP Course](https://huggingface.co/course/chapter1/1)
- [Sentence Transformers](https://www.sbert.net/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

---

<div align="center">

**8 powerful NLP capabilities in one production-ready service**

*Want conversational AI? Try the [LangChain template](../langchain/README.md)*

</div>