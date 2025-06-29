# Llama FastAPI Template

This project was bootstrapped with [FastApi Gen](https://github.com/mirpo/fastapi-gen) using the **llama** template.

## 🚀 Features

This template provides a production-ready FastAPI service with modern llama-cpp-python integration:

### ✅ **Optimized Local LLM Inference**
- **Startup model loading**: Models load once during application startup, not on every request
- **Memory efficient**: Reuses Llama model instances across requests
- **GPU acceleration**: Automatic GPU detection and configurable GPU layer usage
- **Multi-threading**: Configurable thread usage for optimal performance

### ✅ **Advanced llama-cpp-python Configuration**
- **Context window control**: Configurable context size (n_ctx) for longer conversations
- **Performance tuning**: Fine-grained control over threads, GPU layers, and memory usage
- **Model parameters**: Configurable temperature, max tokens, and generation settings
- **Seed control**: Reproducible outputs with configurable random seed

### ✅ **Modern API Design**
- **Dual endpoints**: Both GET and POST (modern) endpoints
- **Request validation**: Pydantic models for type-safe input validation with constraints
- **Response models**: Structured responses with model metadata and token usage
- **Parameter customization**: Override generation parameters per request

### ✅ **Production-Ready Architecture**
- **Lifecycle management**: Proper startup/shutdown handling with async context managers
- **Health monitoring**: `/health` endpoint with detailed model information
- **Structured logging**: Comprehensive logging with proper log levels
- **Error handling**: Graceful error responses with detailed messages
- **Service initialization**: Robust model loading with error recovery

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
Returns service status, model information, context size, GPU configuration, and thread settings.

### Question Answering
```http
# Modern POST endpoint (recommended)
POST /question-answering
Content-Type: application/json

{
  "question": "What is the difference between AI and machine learning?",
  "max_tokens": 150,
  "temperature": 0.7
}

# Legacy GET endpoint
GET /question-answering?question=What is AI?&max_tokens=100&temperature=0.5
```

## ⚙️ Configuration

Configure the model and parameters via environment variables:

```bash
# .env_dev or .env_prod
LLM_MODEL="./models/SmolLM2-135M-Instruct-Q4_K_M.gguf"
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=100
LLM_N_CTX=2048           # Context window size
LLM_N_THREADS=-1         # CPU threads (-1 = auto)
LLM_N_GPU_LAYERS=-1      # GPU layers (-1 = auto, 0 = CPU only)
LLM_VERBOSE=true
LLM_SEED=-1              # Random seed (-1 = random)
```

### Advanced Configuration Options

| Parameter          | Description         | Default     | Notes                           |
| ------------------ | ------------------- | ----------- | ------------------------------- |
| `LLM_N_CTX`        | Context window size | 2048        | Larger values use more memory   |
| `LLM_N_THREADS`    | CPU threads         | -1 (auto)   | Set to number of CPU cores      |
| `LLM_N_GPU_LAYERS` | GPU layers          | -1 (auto)   | 0 = CPU only, higher = more GPU |
| `LLM_SEED`         | Random seed         | -1 (random) | Set for reproducible outputs    |

## Available Scripts

### `make init`
Downloads the model and sets up the environment:
- Creates Python virtual environment
- Installs dependencies from requirements.txt
- Downloads the default SmolLM2 135M model (~0.11GB)

### `make start`
Runs the app in development mode.  
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view OpenAPI documentation.

### `make test`
Runs the comprehensive test suite with real model inference.

### `make lint`
Runs code quality checks with Ruff.

### `make download`
Downloads the model file (automatically detects curl/wget).

## 🔧 Model Management

### Default Model
The template uses **SmolLM2 135M Instruct** quantized to Q4_K_M format:
- **Size**: ~0.11GB download
- **Memory**: ~200MB RAM usage
- **Performance**: Very fast inference on CPU, optimized for speed
- **Quality**: Compact model optimized for efficiency and quick responses

### Using Different Models
1. **Download your model** (GGUF format) to the `./models/` directory
2. **Update configuration**:
   ```bash
   LLM_MODEL="./models/your-model.gguf"
   ```
3. **Adjust settings** based on your model's requirements:
   ```bash
   LLM_N_CTX=4096        # If your model supports larger context
   LLM_N_GPU_LAYERS=32   # Adjust based on your GPU memory
   ```

### GPU Acceleration
- **Automatic detection**: The service automatically detects GPU availability
- **CUDA**: Supported on NVIDIA GPUs with CUDA
- **Metal**: Supported on Apple Silicon Macs
- **Configuration**: Use `LLM_N_GPU_LAYERS` to control GPU usage

## 🧪 Testing Philosophy

This template uses real service testing instead of mocks to ensure:
- ✅ Actual model loading and inference work correctly
- ✅ llama-cpp-python integration functions properly
- ✅ API contracts are validated end-to-end
- ✅ Performance characteristics are realistic

Tests run the actual service with the configured model, providing confidence that your application will work in production.

## 🚀 Production Deployment

### Performance Optimization
- **Model selection**: Choose quantized models (Q4_0, Q5_0) for better performance
- **GPU utilization**: Configure `LLM_N_GPU_LAYERS` based on your hardware
- **Thread optimization**: Set `LLM_N_THREADS` to match your CPU cores
- **Context management**: Balance `LLM_N_CTX` with memory constraints

### Memory Management
- **Model size**: Account for model file size + runtime memory
- **Context scaling**: Larger context windows use exponentially more memory
- **Batch processing**: Single model instance handles multiple concurrent requests

### Security Considerations
- **Model validation**: Ensure model files are from trusted sources
- **Input sanitization**: Built-in request validation prevents malformed inputs
- **Rate limiting**: Consider adding rate limiting for production deployments
- **Access control**: Implement authentication for sensitive deployments

## 🔄 Advanced Features Ready

This template provides a foundation for advanced llama-cpp-python features:
- **Multi-modal support**: Structure ready for image + text models
- **Function calling**: Framework prepared for tool usage
- **JSON schema responses**: Configurable structured outputs
- **Chat completion**: Extensible for conversation management
- **Custom samplers**: Ready for advanced sampling strategies

## 📊 Monitoring

The health endpoint provides comprehensive monitoring data:
- Model initialization status
- Context window configuration
- GPU/CPU resource allocation
- Thread utilization
- Memory usage patterns

Perfect for integration with monitoring systems like Prometheus, Grafana, or cloud monitoring services.