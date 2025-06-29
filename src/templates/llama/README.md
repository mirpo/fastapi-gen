<div align="center">

# 🦙 Llama - Local LLM Powerhouse Template

**Production-ready FastAPI with local LLM inference using llama-cpp-python**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![llama-cpp-python](https://img.shields.io/badge/llama--cpp--python-Latest-blue.svg)](https://github.com/abetlen/llama-cpp-python)
[![GGUF](https://img.shields.io/badge/GGUF-Format-orange.svg)](https://huggingface.co/docs/hub/gguf)

</div>

---

## 🎯 What You'll Build

A **powerful local LLM inference service** with enterprise-grade features:

🏠 **Local LLM Focus** → Optimized for Gemma/Llama GGUF models  
⚡ **GPU Acceleration** → Auto GPU detection, configurable layers  
🎛️ **Advanced Config** → Context windows, threading, performance tuning  
🏗️ **Production Ready** → Lifecycle management, health monitoring  
🧪 **Real Testing** → Actual model inference validation  
🔧 **Easy Setup** → Auto model download, optimized defaults  

## ⚡ Quick Start in 30 Seconds

```bash
# You're already here! First initialize the environment:
make init  # Downloads model (~135MB), sets up environment

# Then start the app:
make start

# Open: http://localhost:8000/docs
```

🚀 **Open:** [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

> 🔄 **First time setup:** `make init` downloads the model and sets up everything (~2-3 minutes).

## 🌟 Local LLM Features

<details>
<summary><strong>🏠 Optimized Local LLM Inference</strong></summary>

**Purpose-built for local models:**
- ✅ **GGUF Format Support** - Optimized for quantized Gemma/Llama models
- ✅ **Startup Model Loading** - Models load once during app startup
- ✅ **Memory Efficient** - Reuses Llama model instances across requests
- ✅ **GPU Acceleration** - Automatic GPU detection and configurable layers
- ✅ **Multi-threading** - Configurable thread usage for optimal performance

**Model Optimizations:**
- Quantized models for speed and memory efficiency
- Smart memory management across requests
- Configurable context windows for longer conversations

</details>

<details>
<summary><strong>⚡ Advanced Configuration</strong></summary>

**Fine-grained performance control:**
- ✅ **Context Window Control** - Configurable n_ctx for longer conversations
- ✅ **GPU Layer Management** - Control how much runs on GPU vs CPU
- ✅ **Thread Optimization** - CPU thread configuration for best performance
- ✅ **Memory Control** - Smart memory allocation and management
- ✅ **Seed Control** - Reproducible outputs with configurable random seed

**Performance Tuning:**
```bash
LLM_N_CTX=2048           # Context window size
LLM_N_THREADS=-1         # CPU threads (-1 = auto)
LLM_N_GPU_LAYERS=-1      # GPU layers (-1 = auto)
LLM_SEED=-1              # Random seed (-1 = random)
```

</details>

<details>
<summary><strong>🏗️ Production-Ready Architecture</strong></summary>

**Enterprise-grade service management:**
- ✅ **Lifecycle Management** - Proper startup/shutdown with async context managers
- ✅ **Health Monitoring** - `/health` endpoint with detailed model information
- ✅ **Structured Logging** - Comprehensive logging with proper levels
- ✅ **Error Handling** - Graceful error responses with detailed messages
- ✅ **Service Initialization** - Robust model loading with error recovery

**Service Features:**
- Automatic model validation on startup
- Graceful degradation and error recovery
- Real-time service status monitoring
- Resource usage tracking

</details>

<details>
<summary><strong>🎛️ Modern API Design</strong></summary>

**Flexible endpoint architecture:**
- ✅ **Dual Endpoints** - Both GET and POST (modern) endpoints
- ✅ **Request Validation** - Pydantic models with type-safe input validation
- ✅ **Response Models** - Structured responses with model metadata and token usage
- ✅ **Parameter Customization** - Override generation parameters per request
- ✅ **Constraint Validation** - Proper limits and validation rules

**API Patterns:**
- Modern: `POST /question-answering` (recommended)
- Legacy: `GET /question-answering?question=...` (for quick testing)

</details>

<details>
<summary><strong>🧪 Real Model Testing</strong></summary>

**Comprehensive validation approach:**
- ✅ **Session-scoped Fixtures** - Efficient test execution with shared model loading
- ✅ **Real Service Testing** - Tests use actual model inference, not mocks
- ✅ **Comprehensive Coverage** - All endpoints, parameters, validation, edge cases
- ✅ **Performance Validation** - Ensures real-world functionality works correctly
- ✅ **Hardware Testing** - Validates GPU/CPU configurations

**Testing Philosophy:**
- Tests actual llama-cpp-python integration
- Validates model loading and inference pipelines
- Ensures API contracts match real model behavior
- Provides confidence for production deployment

</details>

<details>
<summary><strong>🔧 Easy Setup & Management</strong></summary>

**Streamlined development experience:**
- ✅ **Auto Model Download** - Automatic model fetching with make commands
- ✅ **Optimized Defaults** - Sensible default configurations
- ✅ **Environment Detection** - Auto GPU/CPU detection and configuration
- ✅ **Error Recovery** - Robust handling of model loading failures
- ✅ **Development Tools** - Makefile with common development commands

**Setup Features:**
- One-command environment initialization
- Automatic dependency management
- Smart hardware detection and optimization

</details>

## 📡 API Endpoints

### 🏥 Health & Status
```http
GET /health                 # Service status, model info, GPU config, threads
```

### 🤖 Question Answering
```http
# Modern POST endpoint (recommended)
POST /question-answering
Content-Type: application/json

{
  "question": "What is the difference between AI and machine learning?",
  "max_tokens": 150,
  "temperature": 0.7
}

# Legacy GET endpoint (quick testing)
GET /question-answering?question=What%20is%20AI&max_tokens=100&temperature=0.5
```

## 🛠️ Development Commands

<details>
<summary><strong>Available Make Commands</strong></summary>

| Command | Description |
|---------|-------------|
| `make init` | 🚀 Download model and set up environment |
| `make start` | ▶️ Run app in development mode with auto-reload |
| `make test` | 🧪 Run comprehensive test suite with real AI |
| `make lint` | 🔍 Run code quality checks with Ruff |
| `make download` | 📥 Download model file only (auto-detects curl/wget) |

</details>

## 🔧 Configuration & Setup

### Environment Configuration

Create `.env_dev` file:
```bash
# Model configuration
LLM_MODEL="./models/SmolLM2-135M-Instruct-Q4_K_M.gguf"

# Generation parameters
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=100

# Performance tuning
LLM_N_CTX=2048           # Context window size
LLM_N_THREADS=-1         # CPU threads (-1 = auto)
LLM_N_GPU_LAYERS=-1      # GPU layers (-1 = auto, 0 = CPU only)
LLM_VERBOSE=true
LLM_SEED=-1              # Random seed (-1 = random)
```

### Performance Configuration Guide

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `LLM_N_CTX` | Context window size | 2048 | Larger values use more memory |
| `LLM_N_THREADS` | CPU threads | -1 (auto) | Set to number of CPU cores |
| `LLM_N_GPU_LAYERS` | GPU layers | -1 (auto) | 0 = CPU only, higher = more GPU |
| `LLM_SEED` | Random seed | -1 (random) | Set for reproducible outputs |

## 🔧 Model Management

### Default Model: SmolLM2 135M Instruct

**Optimized for development and learning:**
- **Size:** ~135MB download (Q4_K_M quantized)
- **Memory:** ~200MB RAM usage
- **Performance:** Very fast inference on CPU
- **Quality:** Compact model optimized for efficiency

### Using Different Models

1. **Download your GGUF model** to `./models/` directory
2. **Update configuration:**
   ```bash
   LLM_MODEL="./models/your-model.gguf"
   ```
3. **Adjust settings** for your model:
   ```bash
   LLM_N_CTX=4096        # If your model supports larger context
   LLM_N_GPU_LAYERS=32   # Adjust based on your GPU memory
   ```

### Popular Model Options

| Model | Size | Memory | Use Case |
|-------|------|--------|----------|
| SmolLM2-135M | ~135MB | ~200MB | Development, fast inference |
| SmolLM2-360M | ~360MB | ~500MB | Better quality, still fast |
| Llama-3.2-1B | ~1GB | ~1.5GB | Production quality |
| Llama-3.2-3B | ~3GB | ~4GB | High quality responses |

## 🎛️ Hardware Acceleration

### GPU Support

**Automatic Detection:**
- ✅ **CUDA** - NVIDIA GPUs automatically detected
- ✅ **Metal** - Apple Silicon Macs automatically detected  
- ✅ **CPU Fallback** - Graceful fallback to CPU-only mode

**GPU Configuration:**
```bash
# Auto-detect and use all available GPU layers
LLM_N_GPU_LAYERS=-1

# Use specific number of GPU layers
LLM_N_GPU_LAYERS=20

# CPU-only mode
LLM_N_GPU_LAYERS=0
```

### Performance Optimization

**For CPU-only systems:**
```bash
LLM_N_THREADS=8          # Set to your CPU core count
LLM_N_GPU_LAYERS=0       # Disable GPU
LLM_N_CTX=1024          # Smaller context for less memory
```

**For GPU systems:**
```bash
LLM_N_GPU_LAYERS=-1      # Use all GPU layers
LLM_N_CTX=4096          # Larger context with GPU
LLM_N_THREADS=4         # Fewer CPU threads when using GPU
```

## 🧪 Testing Strategy

**Real model validation:**

```bash
make test
# Tests use actual model inference
# First run initializes models (takes longer)
# Subsequent runs are fast (cached models)
```

**What gets tested:**
- ✅ Model loading and initialization
- ✅ Question answering with various parameters
- ✅ Error handling for invalid inputs
- ✅ GPU/CPU configuration validation
- ✅ Context window and threading
- ✅ API contract validation

## 📁 Project Structure

```
llama/
├── main.py              # FastAPI app with llama-cpp-python
├── models/
│   └── SmolLM2-135M-Instruct-Q4_K_M.gguf  # Downloaded model
├── tests/
│   ├── test_main.py     # Real AI integration tests
│   └── __init__.py
├── requirements.txt     # Dependencies (llama-cpp-python, etc.)
├── .env_dev            # Environment configuration
├── Makefile            # Development commands
└── README.md           # This file
```

## 🎓 Local LLM Learning Path

### Mastering Local LLM Inference

1. **🔧 Setup & Configuration**
   - Run `make init` to set up everything
   - Check `/health` endpoint for model and hardware info
   - Experiment with different configuration parameters

2. **🤖 Test Question Answering**
   - Start with simple questions via GET endpoint
   - Move to POST endpoint with custom parameters
   - Experiment with temperature and token limits

3. **⚡ Performance Tuning**
   - Monitor memory usage during inference
   - Test CPU vs GPU performance
   - Optimize thread and layer configurations

4. **🔄 Model Experimentation**
   - Try different GGUF models
   - Compare model sizes vs quality
   - Test context window capabilities

5. **🧪 Run Real Tests**
   - Execute `make test` to see model validation
   - Study test patterns for your own endpoints
   - Understand model loading and inference strategies

## 🚀 Production Deployment

### 🔒 Security Best Practices

- [ ] Implement API key authentication
- [ ] Add rate limiting for inference endpoints
- [ ] Validate and sanitize all text inputs
- [ ] Set up request/response logging
- [ ] Configure CORS for specific domains
- [ ] Monitor model usage and resource consumption

### ⚡ Performance Optimization

- [ ] Use appropriate model quantization (Q4_0, Q5_0, Q8_0)
- [ ] Configure optimal GPU layers for your hardware
- [ ] Set thread count to match CPU cores
- [ ] Balance context window with memory constraints
- [ ] Implement request batching for efficiency
- [ ] Add model response caching for common queries

### 🛠️ Scaling Considerations

- [ ] Plan for model file distribution and caching
- [ ] Set up multiple model instances for load balancing
- [ ] Configure monitoring for memory and GPU usage
- [ ] Implement model warm-up procedures
- [ ] Plan for model updates and versioning
- [ ] Set up backup inference endpoints

## 🔄 Extension Ideas

<details>
<summary><strong>🤖 Advanced LLM Features</strong></summary>

**Ready to implement:**
- Multi-turn conversation with context memory
- Custom prompt templates and formatting
- Function calling and tool usage
- JSON schema-constrained outputs
- Streaming responses for long generations

</details>

<details>
<summary><strong>🏗️ Infrastructure Scaling</strong></summary>

**Production enhancements:**
- Multiple model hosting with model switching
- Load balancing across multiple instances
- Model quantization optimization
- Custom sampling strategies
- Integration with monitoring systems

</details>

<details>
<summary><strong>🔧 Model Management</strong></summary>

**Advanced model operations:**
- Automatic model downloading and caching
- Model validation and testing pipelines
- A/B testing between different models
- Model performance benchmarking
- Custom fine-tuned model integration

</details>

## 🚀 Next Steps

### Explore Other AI Templates

- 🤖 **Comprehensive NLP** - Try the [NLP template](../nlp/README.md) for 8 NLP capabilities
- 🔗 **LangChain Integration** - Check out [LangChain template](../langchain/README.md) for workflows
- 🚀 **Enterprise Features** - Add auth with [Advanced template](../advanced/README.md)

### Learn More About Local LLMs
- 📚 [llama-cpp-python Documentation](https://github.com/abetlen/llama-cpp-python)
- 🦙 [Llama Model Family](https://ai.meta.com/llama/)
- 🔧 [GGUF Format Guide](https://huggingface.co/docs/hub/gguf)
- ⚡ [Quantization Explained](https://huggingface.co/blog/4bit-transformers-bitsandbytes)

---

<div align="center">

**Local LLM power with production-ready patterns** 🦙

*Want cloud-based LLMs? Try the [🔗 LangChain template](../langchain/README.md)*

</div>