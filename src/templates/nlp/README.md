# NLP FastAPI Template

This project was bootstrapped with [FastApi Gen](https://github.com/mirpo/fastapi-gen) using the **nlp** template.

## 🚀 Features

This template provides a production-ready FastAPI service with comprehensive NLP capabilities using modern Transformers:

### ✅ **Comprehensive NLP Pipeline**
- **Text Summarization**: Advanced text summarization using T5-small
- **Named Entity Recognition**: Extract entities (persons, organizations, locations) from text
- **Text Generation**: Creative text generation with SmolLM
- **Question Answering**: Extractive QA using DistilBERT
- **Sentence Embeddings**: Generate dense vector representations using MiniLM
- **Sentiment Analysis**: Classify text sentiment (positive/negative) with DistilBERT
- **Zero-shot Classification**: Classify text into arbitrary categories without training
- **Text Similarity**: Calculate semantic similarity between texts

### ✅ **Production-Ready Architecture**
- **Startup model loading**: All models load once during application startup, not on every request
- **Device auto-detection**: Automatically uses GPU (CUDA/MPS) when available, falls back to CPU
- **Memory efficient**: Reuses model instances across requests for optimal performance
- **Service-based design**: Clean separation of concerns with dedicated NLP service class

### ✅ **Modern API Design**
- **Dual endpoints**: Both GET and POST (modern) endpoints
- **Request validation**: Pydantic models for type-safe input validation with constraints
- **Response models**: Structured responses with model metadata and confidence scores
- **Parameter customization**: Override generation parameters per request
- **Comprehensive error handling**: Graceful error responses with detailed messages

### ✅ **Smart Configuration**
- **Environment-based config**: `.env_dev` and `.env_prod` file support
- **Multiple model options**: Easy configuration for different models per task
- **Configurable parameters**: Generation settings, device selection, and model paths
- **Flexible device targeting**: Auto-detection or manual CPU/GPU/MPS selection

### ✅ **Production Monitoring**
- **Health endpoint**: `/health` with detailed model initialization status
- **Structured logging**: Comprehensive logging with proper log levels
- **Model status tracking**: Real-time monitoring of all loaded models
- **Performance optimization**: Efficient model loading and caching

### ✅ **Enhanced Testing**
- **Session-scoped fixtures**: Efficient test execution with shared model loading
- **Real service testing**: Tests use actual model inference, not mocks
- **Comprehensive coverage**: All endpoints, parameters, validation, and edge cases
- **Performance validation**: Ensures real-world functionality works correctly

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Returns service status, device information, and model loading status.

### Text Summarization
```http
# Modern POST endpoint (recommended)
POST /summarize
Content-Type: application/json

{
  "text": "Long text to summarize here...",
  "max_length": 150
}

# Legacy GET endpoint
GET /summarize?text=Long%20text%20here&max_length=100
```

### Named Entity Recognition
```http
# Modern POST endpoint (recommended)
POST /ner
Content-Type: application/json

{
  "text": "John Smith works at Microsoft in Seattle."
}

# Legacy GET endpoint
GET /ner?text=John%20Smith%20works%20at%20Microsoft
```

### Text Generation
```http
# Modern POST endpoint (recommended)
POST /text-generation
Content-Type: application/json

{
  "text": "The future of artificial intelligence is",
  "max_new_tokens": 100,
  "temperature": 0.7
}

# Legacy GET endpoint
GET /text-generation?text=The%20future%20is&max_new_tokens=50
```

### Question Answering
```http
# Modern POST endpoint (recommended)
POST /question-answering
Content-Type: application/json

{
  "context": "John is a software engineer who lives in San Francisco.",
  "question": "Where does John live?"
}

# Legacy GET endpoint
GET /question-answering?context=John%20lives%20in%20SF&question=Where%20does%20John%20live
```

### Sentence Embeddings
```http
POST /embeddings
Content-Type: application/json

{
  "texts": ["Hello world", "How are you today?"]
}
```

### Sentiment Analysis
```http
POST /sentiment
Content-Type: application/json

{
  "text": "I love this product! It's amazing."
}
```

### Zero-shot Classification
```http
POST /classify
Content-Type: application/json

{
  "text": "I love programming in Python",
  "candidate_labels": ["technology", "sports", "cooking", "programming"]
}
```

### Text Similarity
```http
POST /similarity
Content-Type: application/json

{
  "text1": "The cat is sleeping",
  "text2": "A cat is taking a nap"
}
```

## ⚙️ Configuration

Configure models and parameters via environment variables:

```bash
# .env_dev or .env_prod

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

### Model Alternatives

| Task                   | Default Model                                     | Alternatives                                                               | Notes                                             |
| ---------------------- | ------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------- |
| **Summarization**      | `t5-small`                                        | `facebook/bart-large-cnn`, `google/pegasus-xsum`                           | T5-small fastest, BART better quality             |
| **NER**                | `dslim/bert-base-NER`                             | `dslim/bert-large-NER`, `dbmdz/bert-large-cased-finetuned-conll03-english` | Base version balanced speed/accuracy              |
| **Text Generation**    | `HuggingFaceTB/SmolLM-135M`                       | `openai-community/gpt2`, `microsoft/DialoGPT-small`                        | SmolLM very efficient                             |
| **Question Answering** | `distilbert-base-cased-distilled-squad`           | `distilbert-base-uncased-distilled-squad`                                  | Cased version better for names                    |
| **Embeddings**         | `all-MiniLM-L6-v2`                                | `all-mpnet-base-v2`, `paraphrase-multilingual-MiniLM-L12-v2`               | MiniLM best speed/quality ratio                   |
| **Sentiment**          | `distilbert-base-uncased-finetuned-sst-2-english` | `cardiffnlp/twitter-roberta-base-sentiment-latest`                         | DistilBERT faster                                 |
| **Zero-shot**          | `typeform/distilbert-base-uncased-mnli`           | `facebook/bart-large-mnli`, `microsoft/DialoGPT-medium`                   | DistilBERT smaller and CI-friendly                |

## Available Scripts

### `make init`
Sets up the development environment:
- Creates Python virtual environment
- Installs dependencies from requirements.txt
- Initializes git repository

### `make start`
Runs the app in development mode.  
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view OpenAPI documentation.

### `make test`
Runs the comprehensive test suite with real model inference.

**Note**: Tests automatically use CPU mode to avoid memory issues. To test with GPU locally:
```bash
unset CI && DEVICE=auto make test
```

### `make lint`
Runs code quality checks with Ruff.

## 🔧 Development Notes

### Model Loading Strategy
- **Startup Loading**: All models are loaded during application startup (not on first request)
- **Memory Management**: Models stay in memory for the lifetime of the application
- **Device Optimization**: Automatic detection and utilization of available hardware (GPU/CPU/MPS)
- **Concurrent Requests**: Single model instances handle multiple concurrent requests efficiently

### Performance Characteristics
- **Cold Start**: ~30-60 seconds (depending on models and device)
- **Warm Inference**: <1 second for most operations
- **Memory Usage**: ~2-4GB RAM (varies by selected models)
- **GPU Acceleration**: Automatic when available (CUDA/MPS)

### Hardware Requirements
- **Minimum**: 8GB RAM, CPU-only operation
- **Recommended**: 16GB RAM, GPU with 4GB+ VRAM
- **Apple Silicon**: Excellent performance with MPS acceleration
- **CUDA**: NVIDIA GPUs automatically detected and utilized
- **CI/Testing**: Automatically uses CPU in CI environments to avoid memory issues

## 🧪 Testing Philosophy

This template uses real service testing instead of mocks to ensure:
- ✅ Actual model loading and inference work correctly
- ✅ Transformers pipeline integration functions properly
- ✅ API contracts are validated end-to-end
- ✅ Performance characteristics are realistic
- ✅ Cross-platform compatibility (CPU/GPU/MPS)

Tests run the actual service with the configured models, providing confidence that your application will work in production.

## 🔧 CI/CD Configuration

### GitHub Actions Setup
For CI environments, the template automatically detects and uses CPU-only mode to avoid memory issues:

```yaml
# .github/workflows/test.yml
env:
  CI: true
  DEVICE: cpu  # Force CPU usage in CI
```

The service automatically detects `CI` or `GITHUB_ACTIONS` environment variables and switches to CPU mode.

### Local Testing with CPU
To test locally with CPU mode (matching CI behavior):
```bash
export DEVICE=cpu
make test
```

## 🚀 Production Deployment

### Performance Optimization
- **Model Selection**: Choose smaller models for faster inference (e.g., DistilBERT vs BERT)
- **Device Utilization**: Use GPU acceleration when available
- **Batch Processing**: Group similar requests for better throughput
- **Memory Management**: Monitor memory usage and adjust model selection accordingly

### Scaling Considerations
- **Horizontal Scaling**: Each instance loads models independently
- **Load Balancing**: Distribute requests across multiple instances
- **Caching**: Consider caching frequent embeddings or classifications
- **Model Optimization**: Use quantized or distilled models for production

### Security Best Practices
- **Input Validation**: Built-in request validation prevents malformed inputs
- **Rate Limiting**: Consider adding rate limiting for production deployments
- **Model Verification**: Ensure model files are from trusted sources
- **Access Control**: Implement authentication for sensitive deployments

## 🔄 Advanced Usage Examples

### Batch Processing
```python
# Embed multiple texts efficiently
response = client.post("/embeddings", json={
    "texts": ["Text 1", "Text 2", "Text 3", ...]
})
```

### Custom Model Configuration
```python
# Use different models by updating .env_dev
SUMMARIZE_MODEL="facebook/bart-large-cnn"  # Higher quality
NER_MODEL="dslim/bert-large-NER"          # Better accuracy
```

### Similarity Search
```python
# Calculate semantic similarity
response = client.post("/similarity", json={
    "text1": "Machine learning is fascinating",
    "text2": "AI and ML are interesting topics"
})
# Returns similarity score between 0-1
```

### Zero-shot Classification
```python
# Classify without training data
response = client.post("/classify", json={
    "text": "The stock market is performing well today",
    "candidate_labels": ["finance", "sports", "technology", "politics"]
})
# Returns ranked labels with confidence scores
```

## 📊 Model Information

### Default Model Sizes
- **T5-small**: ~240MB, 60M parameters
- **DistilBERT models**: ~250MB, 66M parameters each
- **SmolLM-135M**: ~270MB, 135M parameters
- **DistilBERT-mnli**: ~250MB, 66M parameters
- **all-MiniLM-L6-v2**: ~90MB, 22M parameters

### Total Resource Usage
- **Models on Disk**: ~1.5-2GB total
- **Memory Usage**: ~2-4GB RAM when loaded
- **GPU Memory**: 2-6GB VRAM (if using GPU acceleration)

This template provides a comprehensive NLP service that can handle most common text processing tasks while maintaining excellent performance and production readiness.