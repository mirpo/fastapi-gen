import logging
from contextlib import asynccontextmanager

import torch
from fastapi import Depends, FastAPI, HTTPException
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env_dev", ".env.prod"),
    )
    text_generation_model: str
    device: str = "auto"
    max_new_tokens: int = 100
    max_length: int = 150
    no_repeat_ngram_size: int = 2
    temperature: float = 0.7
    random_seed: int = 42

    def get_device(self) -> str:
        if self.device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return self.device


class TextGenerationRequest(BaseModel):
    text: str = Field(..., description="Input text for generation")
    max_new_tokens: int | None = Field(None, description="Maximum new tokens to generate")
    temperature: float | None = Field(None, description="Generation temperature")


class QuestionAnsweringRequest(BaseModel):
    context: str = Field(..., description="Context for question answering")
    question: str = Field(..., description="Question to answer")
    max_new_tokens: int | None = Field(None, description="Maximum new tokens to generate")
    temperature: float | None = Field(None, description="Generation temperature")


class GenerationResponse(BaseModel):
    prompt: str
    answer: str
    model_used: str


class QAResponse(BaseModel):
    context: str
    question: str
    answer: str
    model_used: str


class LangChainService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.device = settings.get_device()
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.llm = None

    async def initialize(self):
        """Initialize model and pipeline on startup"""
        try:
            logger.info(f"Loading model {self.settings.text_generation_model} on {self.device}")
            set_seed(self.settings.random_seed)

            self.tokenizer = AutoTokenizer.from_pretrained(self.settings.text_generation_model)
            self.model = AutoModelForCausalLM.from_pretrained(self.settings.text_generation_model).to(self.device)

            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=self.settings.max_new_tokens,
                max_length=self.settings.max_length,
                no_repeat_ngram_size=self.settings.no_repeat_ngram_size,
                early_stopping=True,
            )
            self.llm = HuggingFacePipeline(pipeline=self.pipeline)
            logger.info("Model initialization completed successfully")
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise

    def generate_text(self, text: str, max_new_tokens: int | None = None, temperature: float | None = None) -> str:
        """Generate text using the loaded model"""
        if not self.llm:
            raise HTTPException(status_code=503, detail="Model not initialized")

        try:
            template = "{text}"
            prompt = PromptTemplate(input_variables=["text"], template=template)
            chain = prompt | self.llm
            result = chain.invoke({"text": text}).strip()
            return result
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")

    def answer_question(
        self, context: str, question: str, max_new_tokens: int | None = None, temperature: float | None = None
    ) -> str:
        """Answer question based on context"""
        if not self.llm:
            raise HTTPException(status_code=503, detail="Model not initialized")

        try:
            template = "Context: {context}\nQuestion: {question}\nAnswer:"
            prompt = PromptTemplate(input_variables=["context", "question"], template=template)
            chain = prompt | self.llm
            result = chain.invoke({"context": context, "question": question}).strip()
            return result
        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            raise HTTPException(status_code=500, detail=f"QA failed: {e!s}")


langchain_service = None
settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global langchain_service
    langchain_service = LangChainService(settings)
    await langchain_service.initialize()
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="LangChain FastAPI Service",
    description="FastAPI service with LangChain integration for text generation and QA",
    version="1.0.0",
    lifespan=lifespan,
)


def get_langchain_service() -> LangChainService:
    if langchain_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return langchain_service


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": settings.text_generation_model, "device": settings.get_device()}


@app.post("/text-generation", response_model=GenerationResponse)
async def text_generation(
    request: TextGenerationRequest,
    service: LangChainService = Depends(get_langchain_service),
) -> GenerationResponse:
    """Generate text based on input prompt"""
    try:
        result = service.generate_text(
            request.text,
            request.max_new_tokens,
            request.temperature,
        )
        return GenerationResponse(
            prompt=request.text,
            answer=result,
            model_used=settings.text_generation_model,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in text generation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/text-generation")
async def text_generation_get(
    text: str,
    service: LangChainService = Depends(get_langchain_service),
) -> GenerationResponse:
    """Generate text based on query parameter"""
    request = TextGenerationRequest(text=text)
    return await text_generation(request, service)


@app.post("/question-answering", response_model=QAResponse)
async def question_answering(
    request: QuestionAnsweringRequest,
    service: LangChainService = Depends(get_langchain_service),
) -> QAResponse:
    """Answer questions based on provided context"""
    try:
        result = service.answer_question(
            request.context,
            request.question,
            request.max_new_tokens,
            request.temperature,
        )
        return QAResponse(
            context=request.context,
            question=request.question,
            answer=result,
            model_used=settings.text_generation_model,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in question answering: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/question-answering")
async def question_answering_get(
    context: str,
    question: str,
    service: LangChainService = Depends(get_langchain_service),
) -> QAResponse:
    """Answer questions based on query parameters"""
    request = QuestionAnsweringRequest(context=context, question=question)
    return await question_answering(request, service)
