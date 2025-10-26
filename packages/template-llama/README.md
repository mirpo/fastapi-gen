<div align="center">

# Llama - Local LLM Powerhouse Template

**Production-ready FastAPI with local LLM inference using llama-cpp-python**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![llama-cpp-python](https://img.shields.io/badge/llama--cpp--python-Latest-blue.svg)](https://github.com/abetlen/llama-cpp-python)

</div>

---

## What You'll Build

A powerful local LLM inference service optimized for Gemma/Llama GGUF models with GPU acceleration, advanced configuration for context windows and threading, production-ready lifecycle management, real testing with actual inference, and easy setup with auto model download.

## Quick Start

```bash
# Install dependencies:
make install

# Download the model (~135MB):
make download

# Start the app:
make start
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

> **macOS ARM64 Note**: If `make install` fails to compile llama-cpp-python, set these flags first:
> ```bash
> export CFLAGS="-march=armv8.2-a+simd"
> export CXXFLAGS="-march=armv8.2-a+simd"
> export CMAKE_ARGS="-DGGML_METAL=OFF"
> make install
> ```

## Local LLM Features

**Optimized Local LLM Inference**
- GGUF format support for quantized Gemma/Llama models
- Startup model loading (models load once during app startup)
- Memory efficient with reused Llama instances
- GPU acceleration with automatic detection
- Multi-threading with configurable thread usage

**Advanced Configuration**
- Context window control (configurable n_ctx for longer conversations)
- GPU layer management (control how much runs on GPU vs CPU)
- Thread optimization (CPU thread configuration)
- Memory control with smart allocation
- Seed control for reproducible outputs

**Production Architecture**
- Lifecycle management with proper startup/shutdown
- Health monitoring at `/health` endpoint
- Structured logging with proper levels
- Graceful error handling and recovery
- Service initialization with validation

**Modern API Design**
- Dual endpoints (GET for testing, POST for production)
- Pydantic models with type-safe validation
- Structured responses with model metadata
- Parameter customization per request
- Constraint validation and limits

**Real Model Testing**
- Session-scoped fixtures for efficient test execution
- Tests use actual model inference (not mocks)
- Comprehensive coverage of endpoints and parameters
- Performance validation for real-world scenarios
- Hardware testing for GPU/CPU configurations

**Easy Setup**
- Auto model download with simple commands
- Optimized default configurations
- Environment detection for hardware
- Error recovery for failed model loads
- Make commands for common tasks

## API Endpoints

### Health & Status
```http
GET /health                 # Service status, model info, GPU config, threads
```

### Question Answering
```http
# Modern POST endpoint (recommended)
POST /question-answering
{
  "question": "What is the difference between AI and machine learning?",
  "max_tokens": 150,
  "temperature": 0.7
}

# Legacy GET endpoint (quick testing)
GET /question-answering?question=What%20is%20AI&max_tokens=100&temperature=0.5
```

## Development Commands

| Command         | Description                                  |
| --------------- | -------------------------------------------- |
| `make install`  | Install dependencies and set up environment  |
| `make start`    | Run app in development mode with auto-reload |
| `make test`     | Run comprehensive test suite with real AI    |
| `make lint`     | Run code quality checks with Ruff            |
| `make lint-fix` | Auto-fix linting issues and format code      |
| `make download` | Download model (~135MB)                      |

**Manual model download** (alternative to `make download`):
```bash
mkdir -p models
curl -L https://huggingface.co/bartowski/SmolLM2-135M-Instruct-GGUF/resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf -o models/SmolLM2-135M-Instruct-Q4_K_M.gguf
```

## Configuration

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

### Performance Configuration

| Parameter          | Description         | Default     | Notes                           |
| ------------------ | ------------------- | ----------- | ------------------------------- |
| `LLM_N_CTX`        | Context window size | 2048        | Larger values use more memory   |
| `LLM_N_THREADS`    | CPU threads         | -1 (auto)   | Set to number of CPU cores      |
| `LLM_N_GPU_LAYERS` | GPU layers          | -1 (auto)   | 0 = CPU only, higher = more GPU |
| `LLM_SEED`         | Random seed         | -1 (random) | Set for reproducible outputs    |

## Model Management

### Default Model: SmolLM2 135M Instruct

Optimized for development and learning:
- **Size**: ~135MB download (Q4_K_M quantized)
- **Memory**: ~200MB RAM usage
- **Performance**: Very fast inference on CPU
- **Quality**: Compact model optimized for efficiency

### Using Different Models

1. Download your GGUF model to `./models/` directory
2. Update configuration: `LLM_MODEL="./models/your-model.gguf"`
3. Adjust settings based on your model:
   - `LLM_N_CTX=4096` (if model supports larger context)
   - `LLM_N_GPU_LAYERS=32` (adjust based on GPU memory)

### Popular Model Options

| Model        | Size   | Memory | Use Case                    |
| ------------ | ------ | ------ | --------------------------- |
| SmolLM2-135M | ~135MB | ~200MB | Development, fast inference |
| SmolLM2-360M | ~360MB | ~500MB | Better quality, still fast  |
| Llama-3.2-1B | ~1GB   | ~1.5GB | Production quality          |
| Llama-3.2-3B | ~3GB   | ~4GB   | High quality responses      |

## Hardware Acceleration

**GPU Support**
- CUDA (NVIDIA GPUs) automatically detected
- Metal (Apple Silicon Macs) automatically detected
- CPU fallback for systems without GPU

**GPU Configuration**:
```bash
# Auto-detect and use all available GPU layers
LLM_N_GPU_LAYERS=-1

# Use specific number of GPU layers
LLM_N_GPU_LAYERS=20

# CPU-only mode
LLM_N_GPU_LAYERS=0
```

**Performance Optimization**:

For CPU-only systems:
```bash
LLM_N_THREADS=8          # Set to your CPU core count
LLM_N_GPU_LAYERS=0       # Disable GPU
LLM_N_CTX=1024          # Smaller context for less memory
```

For GPU systems:
```bash
LLM_N_GPU_LAYERS=-1      # Use all GPU layers
LLM_N_CTX=4096          # Larger context with GPU
LLM_N_THREADS=4         # Fewer CPU threads when using GPU
```

## Testing

Tests use actual model inference (not mocks):

```bash
make test
# First run initializes models (takes longer)
# Subsequent runs use cached models
```

## Project Structure

```
llama/
├── src/
│   └── llama_app/
│       ├── __init__.py
│       └── main.py      # FastAPI app with llama-cpp-python
├── tests/
│   ├── test_main.py     # Real AI integration tests
│   └── __init__.py
├── pyproject.toml       # Project configuration (uv)
├── .env_dev             # Environment configuration
├── Makefile             # Development commands
├── .gitignore
└── README.md            # This file

# Auto-generated at runtime:
└── models/              # Downloaded GGUF models
    └── SmolLM2-135M-Instruct-Q4_K_M.gguf
```
