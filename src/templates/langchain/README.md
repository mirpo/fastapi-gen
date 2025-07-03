<div align="center">

# LangChain - Modern LLM Integration Template

**Production-ready FastAPI with LangChain for LLM workflows**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-purple.svg)](https://python.langchain.com)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.0+-orange.svg)](https://huggingface.co/transformers)

</div>

---

## What You'll Build

A **modern LangChain-powered FastAPI service** with production-ready LLM integration:

**Optimized Loading** → Models load at startup, not per request  
**Modern Patterns** → Latest LangChain 0.3.x best practices  
**Smart Configuration** → Auto device detection (CPU/GPU)  
**Dual Endpoints** → Text generation & question answering  
**Production Ready** → Health checks, monitoring, error handling  
**Real AI Testing** → Actual model inference validation  

## Quick Start in 30 Seconds

```bash
# You're already here! Just run:
make start

# The app will download models on first startup (be patient!)
# Then open: http://localhost:8000/docs
```

**Open:** [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

> **First startup:** Downloads models (~1-2GB), takes 2-3 minutes depending on internet speed.

## LangChain Features

<details>
<summary><strong>Optimized Model Loading</strong></summary>

**Smart startup patterns:**
- ✅ **Startup Caching** - Models load once during app startup
- ✅ **Memory Efficient** - Reuses tokenizer and model instances
- ✅ **Error Handling** - Graceful initialization with detailed logging
- ✅ **Device Detection** - Automatic GPU/CPU selection
- ✅ **Connection Pooling** - Efficient model instance management

**Performance Benefits:**
- First request: Instant (models already loaded)
- Memory usage: Optimized for concurrent requests
- Startup time: 30-60 seconds (one-time model download)

</details>

<details>
<summary><strong>Modern LangChain Patterns</strong></summary>

**Latest LangChain 0.3.x features:**
- ✅ **Updated Imports** - Uses `langchain-huggingface` (not deprecated `langchain-community`)
- ✅ **Current API** - Modern LangChain patterns and method calls
- ✅ **Type Safety** - Full Pydantic integration for requests/responses
- ✅ **Error Handling** - Proper exception management
- ✅ **Async Support** - Non-blocking operations where possible

**Modern Code Structure:**
```python
from langchain_huggingface import HuggingFacePipeline
# Latest imports, not legacy ones
```

</details>

<details>
<summary><strong>Smart Configuration</strong></summary>

**Intelligent setup:**
- ✅ **Auto Device Detection** - GPU when available, CPU fallback
- ✅ **Environment Config** - `.env_dev` and `.env_prod` support
- ✅ **Model Selection** - Configurable model paths and parameters
- ✅ **Generation Settings** - Temperature, max tokens, and more
- ✅ **Runtime Overrides** - Request-level parameter customization

**Configuration Options:**
```bash
TEXT_GENERATION_MODEL="HuggingFaceTB/SmolLM2-360M-Instruct"
DEVICE="auto"  # auto, cpu, or cuda
MAX_NEW_TOKENS=100
TEMPERATURE=0.7
```

</details>

<details>
<summary><strong>Dual AI Endpoints</strong></summary>

**Two complementary LLM use cases:**
- ✅ **Text Generation** - Creative text completion and generation
- ✅ **Question Answering** - Context-based question answering
- ✅ **Flexible Input** - Both GET and POST endpoints
- ✅ **Parameter Control** - Override defaults per request
- ✅ **Structured Output** - Consistent response formats

**Endpoint Types:**
- Modern: `POST /text-generation` (recommended)
- Legacy: `GET /text-generation?text=...` (for quick testing)

</details>

<details>
<summary><strong>Production Monitoring</strong></summary>

**Enterprise-ready observability:**
- ✅ **Health Endpoint** - `/health` with model status and device info
- ✅ **Structured Logging** - Comprehensive logging with proper levels
- ✅ **Error Responses** - Detailed error messages for debugging
- ✅ **Service Status** - Real-time model and configuration information
- ✅ **Performance Metrics** - Ready for monitoring integration

**Health Check Data:**
- Model initialization status
- Device configuration (CPU/GPU)
- Available memory and resources
- Service uptime and readiness

</details>

<details>
<summary><strong>Real AI Testing</strong></summary>

**Comprehensive test strategy:**
- ✅ **Integration Tests** - Tests use actual model inference (not mocks)
- ✅ **Endpoint Coverage** - All endpoints, parameters, and edge cases tested
- ✅ **Performance Validation** - Ensures real-world functionality
- ✅ **Session Fixtures** - Efficient test execution with shared model loading
- ✅ **Error Testing** - Invalid input and edge case handling

**Why Real Testing:**
- Validates actual LangChain integration works
- Ensures API contracts match real model behavior
- Catches model loading and inference issues
- Provides confidence for production deployment

</details>

## API Endpoints

### Health & Status
```http
GET /health                 # Service status, model info, device config
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

# Legacy GET endpoint (quick testing)
GET /text-generation?text=What%20is%20AI&max_new_tokens=50
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

# Legacy GET endpoint (quick testing)
GET /question-answering?context=AI%20is...&question=What%20is%20AI?
```

## Development Commands

<details>
<summary><strong>Available Make Commands</strong></summary>

| Command | Description |
|---------|-------------|
| `make start` | Run app in development mode with auto-reload |
| `make test` | Run comprehensive test suite with real AI |
| `make lint` | Run code quality checks with Ruff |

</details>

## Configuration & Setup

### Environment Configuration

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

| Model | Size | Use Case | Memory |
|-------|------|----------|--------|
| `SmolLM2-360M-Instruct` | 360M | Fast inference, development | ~1GB |
| `SmolLM2-1.7B-Instruct` | 1.7B | Better quality, production | ~3GB |
| `microsoft/DialoGPT-small` | 345M | Conversational AI | ~1GB |

### Hardware Requirements

- **Minimum:** 4GB RAM, CPU-only operation
- **Recommended:** 8GB+ RAM, GPU with 2GB+ VRAM
- **GPU Support:** CUDA (NVIDIA) automatically detected
- **Apple Silicon:** Excellent performance with MPS

## Testing Philosophy

**Real AI validation approach:**

```bash
make test
# Tests download and use actual models
# First run takes longer (model download)
# Subsequent runs are fast (cached models)
```

**What gets tested:**
- ✅ Model loading and initialization
- ✅ Text generation with various parameters  
- ✅ Question answering accuracy
- ✅ Error handling for invalid inputs
- ✅ Device selection and configuration
- ✅ API contract validation

## Project Structure

```
langchain/
├── main.py              # FastAPI app with LangChain integration
├── tests/
│   ├── test_main.py     # Real AI integration tests
│   └── __init__.py
├── requirements.txt     # Dependencies (LangChain, transformers, etc.)
├── .env_dev            # Environment configuration
├── Makefile            # Development commands
└── README.md           # This file
```

## LangChain Learning Path

### Mastering LLM Integration

1. **Explore Configuration**
   - Check `/health` endpoint for model and device info
   - Try different models in `.env_dev`
   - Experiment with generation parameters

2. **Test Text Generation**
   - Start with simple prompts via GET endpoint
   - Move to POST endpoint with custom parameters
   - Experiment with temperature and token limits

3. **Master Question Answering**
   - Provide context and ask specific questions
   - Try different context lengths
   - Compare answers with different models

4. **Performance Tuning**
   - Monitor memory usage during inference
   - Test concurrent requests
   - Compare CPU vs GPU performance

5. **Run Real Tests**
   - Execute `make test` to see AI validation
   - Study test patterns for your own endpoints
   - Understand model loading strategies

## Production Deployment

### Security Best Practices

- [ ] Implement API key authentication
- [ ] Add rate limiting for inference endpoints
- [ ] Validate and sanitize all text inputs
- [ ] Set up request/response logging
- [ ] Configure CORS for specific domains
- [ ] Monitor model usage and costs

### Performance Optimization

- [ ] Use GPU acceleration when available
- [ ] Implement request batching for efficiency
- [ ] Add model response caching
- [ ] Set up model serving with multiple workers
- [ ] Monitor memory usage and optimize
- [ ] Consider model quantization for speed

### Scaling Considerations

- [ ] Set up multiple model instances
- [ ] Implement load balancing
- [ ] Add model warm-up procedures
- [ ] Configure monitoring and alerting
- [ ] Plan for model updates and versioning
- [ ] Set up backup inference endpoints

## Extension Ideas

<details>
<summary><strong>Advanced LLM Features</strong></summary>

**Ready to implement:**
- Conversation memory and context
- Multi-turn dialogue systems
- Custom fine-tuned models
- Prompt template management
- Response streaming for long outputs

</details>

<details>
<summary><strong>LangChain Ecosystem</strong></summary>

**LangChain integrations:**
- Vector stores for document QA
- Agent systems with tool usage
- Chain composition and workflows
- Memory management systems
- Custom retrieval augmented generation (RAG)

</details>

<details>
<summary><strong>Production Features</strong></summary>

**Enterprise enhancements:**
- Model A/B testing frameworks
- Usage analytics and billing
- Multi-model inference endpoints
- Custom model serving pipelines
- Integration with ML monitoring tools

</details>

## Next Steps

### Explore Other AI Templates

- **Text Processing** - Try the [NLP template](../nlp/README.md) for 8 NLP capabilities
- **Local LLM** - Check out [Llama template](../llama/README.md) for local inference
- **Enterprise Features** - Add auth with [Advanced template](../advanced/README.md)

### Learn More LangChain
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangChain Tutorials](https://python.langchain.com/docs/tutorials/)
- [LangChain Community](https://github.com/langchain-ai/langchain)

---

<div align="center">

**Modern LangChain integration with production-ready patterns**

*Want local LLM control? Try the [Llama template](../llama/README.md)*

</div>