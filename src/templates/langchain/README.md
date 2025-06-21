# LangChain FastAPI Template

This project was bootstrapped with [FastApi Gen](https://github.com/mirpo/fastapi-gen) using the **langchain** template.

## 🚀 Features

This template provides a production-ready FastAPI service with modern LangChain integration:

### ✅ **Optimized Model Loading**
- **Startup caching**: Models load once during application startup, not on every request
- **Memory efficient**: Reuses tokenizer and model instances across requests
- **Error handling**: Graceful initialization with detailed logging

### ✅ **Modern LangChain Patterns**
- **Updated imports**: Uses `langchain-huggingface` instead of deprecated `langchain-community`
- **Current API**: Latest LangChain 0.3.x patterns and best practices
- **Type safety**: Full Pydantic integration for request/response models

### ✅ **Flexible API Design**
- **Dual endpoints**: Both GET (backward compatibility) and POST (modern) endpoints
- **Request validation**: Pydantic models for type-safe input validation
- **Response models**: Structured responses with model metadata
- **Parameter customization**: Override generation parameters per request

### ✅ **Smart Configuration**
- **Auto device detection**: Automatically uses GPU when available, falls back to CPU
- **Environment-based config**: `.env_dev` and `.env_prod` file support
- **Configurable parameters**: Generation settings, model paths, and device selection

### ✅ **Production Monitoring**
- **Health endpoint**: `/health` for service monitoring and readiness checks
- **Structured logging**: Comprehensive logging with proper log levels
- **Error handling**: Graceful error responses with detailed messages
- **Service status**: Real-time model and device information

### ✅ **Real Service Testing**
- **Integration tests**: Tests use actual model inference, not mocks
- **Comprehensive coverage**: All endpoints, parameters, and edge cases
- **Performance validation**: Ensures real-world functionality
- **Session-scoped fixtures**: Efficient test execution with shared model loading

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Returns service status, model information, and device configuration.

### Text Generation
```http
# Modern POST endpoint (recommended)
POST /text-generation
Content-Type: application/json

{
  "text": "What is artificial intelligence?",
  "max_new_tokens": 100,
  "temperature": 0.7
}

# Legacy GET endpoint (backward compatibility)
GET /text-generation?text=What is artificial intelligence?
```

### Question Answering
```http
# Modern POST endpoint (recommended)
POST /question-answering
Content-Type: application/json

{
  "context": "AI is a field of computer science focused on creating intelligent machines.",
  "question": "What is AI?",
  "max_new_tokens": 50
}

# Legacy GET endpoint (backward compatibility)
GET /question-answering?context=AI is...&question=What is AI?
```

## ⚙️ Configuration

Configure the model and parameters via environment variables:

```bash
# .env_dev or .env_prod
TEXT_GENERATION_MODEL="HuggingFaceTB/SmolLM2-360M-Instruct"
DEVICE="auto"  # auto, cpu, or cuda
MAX_NEW_TOKENS=100
MAX_LENGTH=150
TEMPERATURE=0.7
RANDOM_SEED=42
```

## Available Scripts

### `make start`
Runs the app in development mode.  
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view OpenAPI documentation.

### `make test`
Runs the comprehensive test suite with real model inference.

### `make lint`
Runs code quality checks with Ruff.

## 🔧 Development Notes

- **Model Loading**: The service downloads and caches the Hugging Face model on first startup
- **Memory Usage**: Expect ~1-2GB RAM usage depending on the model size
- **GPU Support**: Automatically detected and used when available
- **Performance**: Models are loaded once and reused across all requests for optimal performance

## 🧪 Testing Philosophy

This template uses real service testing instead of mocks to ensure:
- ✅ Actual model loading and inference work correctly
- ✅ LangChain integration functions properly
- ✅ API contracts are validated end-to-end
- ✅ Performance characteristics are realistic

Tests run the actual service with the configured model, providing confidence that your application will work in production.