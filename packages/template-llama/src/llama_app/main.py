import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from llama_cpp import Llama
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env_dev", ".env.prod"),
    )
    llm_model: str
    llm_temperature: float = 0.7
    llm_max_tokens: int = 100
    llm_n_ctx: int = 2048
    llm_n_threads: int = -1
    llm_n_gpu_layers: int = -1
    llm_verbose: bool = True
    llm_seed: int = -1


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Question to ask the model")
    max_tokens: int | None = Field(None, gt=0, le=2048, description="Maximum tokens to generate")
    temperature: float | None = Field(None, ge=0.0, le=2.0, description="Sampling temperature")


class QuestionResponse(BaseModel):
    question: str
    answer: str
    model_used: str
    tokens_generated: int | None = None


class HealthResponse(BaseModel):
    status: str
    model: str
    context_size: int
    gpu_layers: int
    threads: int


class LlamaService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm: Llama | None = None

    async def initialize(self):
        """Initialize Llama model on startup"""
        try:
            logger.info(f"Loading model {self.settings.llm_model}")
            logger.info(f"Context size: {self.settings.llm_n_ctx}")
            logger.info(f"GPU layers: {self.settings.llm_n_gpu_layers}")
            logger.info(f"Threads: {self.settings.llm_n_threads}")

            self.llm = Llama(
                model_path=self.settings.llm_model,
                n_ctx=self.settings.llm_n_ctx,
                n_threads=self.settings.llm_n_threads,
                n_gpu_layers=self.settings.llm_n_gpu_layers,
                seed=self.settings.llm_seed,
                verbose=self.settings.llm_verbose,
            )
            logger.info("Model initialization completed successfully")
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise

    def generate_answer(
        self,
        question: str,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> dict[str, Any]:
        """Generate answer using the loaded model"""
        if not self.llm:
            raise HTTPException(status_code=503, detail="Model not initialized")

        try:
            # Use provided parameters or fall back to settings
            actual_max_tokens = max_tokens or self.settings.llm_max_tokens
            actual_temperature = temperature or self.settings.llm_temperature

            prompt = f"""### Instruction:
{question}

### Response:

"""

            result = self.llm(
                prompt,
                max_tokens=actual_max_tokens,
                temperature=actual_temperature,
                echo=True,
            )

            # Extract the response part after "### Response:"
            full_text = result["choices"][0]["text"]
            if "### Response:" in full_text:
                answer = full_text.split("### Response:")[1].strip()
            else:
                answer = full_text.strip()

            return {
                "answer": answer,
                "tokens_generated": result["usage"]["completion_tokens"] if "usage" in result else None,
            }
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")

    def get_model_info(self) -> dict[str, Any]:
        """Get model information for health checks"""
        if not self.llm:
            return {"initialized": False}

        return {
            "initialized": True,
            "model_path": self.settings.llm_model,
            "context_size": self.settings.llm_n_ctx,
            "gpu_layers": self.settings.llm_n_gpu_layers,
            "threads": self.settings.llm_n_threads,
        }


llama_service = None
settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global llama_service
    llama_service = LlamaService(settings)
    await llama_service.initialize()
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="Llama FastAPI Service",
    description="FastAPI service with llama-cpp-python integration for local LLM inference",
    version="1.0.0",
    lifespan=lifespan,
)


def get_llama_service() -> LlamaService:
    if llama_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return llama_service


@app.get("/health", response_model=HealthResponse)
async def health_check(service: LlamaService = Depends(get_llama_service)):
    """Health check endpoint with model information"""
    model_info = service.get_model_info()

    if not model_info["initialized"]:
        raise HTTPException(status_code=503, detail="Model not initialized")

    return HealthResponse(
        status="healthy",
        model=settings.llm_model,
        context_size=settings.llm_n_ctx,
        gpu_layers=settings.llm_n_gpu_layers,
        threads=settings.llm_n_threads,
    )


@app.post("/question-answering", response_model=QuestionResponse)
async def question_answering_post(
    request: QuestionRequest,
    service: LlamaService = Depends(get_llama_service),
) -> QuestionResponse:
    """Answer questions using the Llama model (modern POST endpoint)"""
    try:
        result = service.generate_answer(
            request.question,
            request.max_tokens,
            request.temperature,
        )

        return QuestionResponse(
            question=request.question,
            answer=result["answer"],
            model_used=settings.llm_model,
            tokens_generated=result["tokens_generated"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in question answering: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/question-answering", response_model=QuestionResponse)
async def question_answering_get(
    question: str,
    max_tokens: int | None = None,
    temperature: float | None = None,
    service: LlamaService = Depends(get_llama_service),
) -> QuestionResponse:
    """Answer questions using query parameters"""
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Question must be specified.")

    request = QuestionRequest(
        question=question,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return await question_answering_post(request, service)
