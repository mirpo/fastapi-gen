import logging
import os
from contextlib import asynccontextmanager
from typing import Any

import torch
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env_dev", ".env.prod"),
    )
    summarize_model: str
    ner_model: str
    text_generation_model: str
    qa_model: str
    embedding_model: str
    sentiment_model: str
    zero_shot_model: str
    device: str = "auto"
    max_length: int = 512
    temperature: float = 0.7
    top_p: float = 0.9

    def get_device(self) -> str:
        if self.device == "auto":
            # Force CPU in CI environments to avoid memory issues
            if os.getenv("CI") or os.getenv("GITHUB_ACTIONS"):
                return "cpu"
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        return self.device


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=200, description="Text to summarize (minimum 200 characters)")
    max_length: int | None = Field(None, gt=0, le=512, description="Maximum summary length")


class SummarizeResponse(BaseModel):
    prompt: str
    summary_text: str
    model_used: str


class NERRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text for named entity recognition")


class NERResponse(BaseModel):
    text: str
    entities: list[dict[str, Any]]
    model_used: str


class TextGenerationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Prompt text for generation")
    max_new_tokens: int | None = Field(None, gt=0, le=200, description="Maximum new tokens to generate")
    temperature: float | None = Field(None, ge=0.0, le=2.0, description="Generation temperature")


class TextGenerationResponse(BaseModel):
    prompt: str
    generated_text: str
    model_used: str


class QuestionAnsweringRequest(BaseModel):
    context: str = Field(..., min_length=1, description="Context text")
    question: str = Field(..., min_length=1, description="Question to answer")


class QuestionAnsweringResponse(BaseModel):
    context: str
    question: str
    answer: str
    confidence: float
    model_used: str


class EmbeddingRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, description="List of texts to embed")


class EmbeddingResponse(BaseModel):
    texts: list[str]
    embeddings: list[list[float]]
    model_used: str
    dimension: int


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text for sentiment analysis")


class SentimentResponse(BaseModel):
    text: str
    label: str
    confidence: float
    model_used: str


class ZeroShotRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to classify")
    candidate_labels: list[str] = Field(..., min_length=1, description="List of possible labels")


class ZeroShotResponse(BaseModel):
    text: str
    labels: list[str]
    scores: list[float]
    model_used: str


class SimilarityRequest(BaseModel):
    text1: str = Field(..., min_length=1, description="First text")
    text2: str = Field(..., min_length=1, description="Second text")


class SimilarityResponse(BaseModel):
    text1: str
    text2: str
    similarity: float
    model_used: str


class HealthResponse(BaseModel):
    status: str
    device: str
    models_loaded: dict[str, bool]


class NLPService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.device = settings.get_device()
        self.pipelines: dict[str, Any] = {}
        self.tokenizers: dict[str, Any] = {}
        self.models: dict[str, Any] = {}
        self.sentence_transformer: SentenceTransformer | None = None

    async def initialize(self):
        """Initialize all models and pipelines on startup"""
        try:
            logger.info(f"Initializing NLP service on device: {self.device}")
            set_seed(42)

            # Force CPU for CI environments by setting torch device
            if self.device == "cpu" or os.getenv("CI") or os.getenv("GITHUB_ACTIONS"):
                logger.info("Setting torch to use CPU for CI environment")
                torch.set_default_device("cpu")

            # Initialize pipelines with explicit device
            device_arg = 0 if self.device == "cuda" else -1 if self.device == "cpu" else -1

            logger.info("Loading summarization pipeline...")
            self.pipelines["summarize"] = pipeline(
                "summarization", model=self.settings.summarize_model, device=device_arg
            )

            logger.info("Loading NER pipeline...")
            self.pipelines["ner"] = pipeline(
                "ner", model=self.settings.ner_model, aggregation_strategy="simple", device=device_arg
            )

            logger.info("Loading QA pipeline...")
            self.pipelines["qa"] = pipeline("question-answering", model=self.settings.qa_model, device=device_arg)

            logger.info("Loading sentiment pipeline...")
            self.pipelines["sentiment"] = pipeline(
                "sentiment-analysis", model=self.settings.sentiment_model, device=device_arg
            )

            logger.info("Loading zero-shot pipeline...")
            self.pipelines["zero_shot"] = pipeline(
                "zero-shot-classification", model=self.settings.zero_shot_model, device=device_arg
            )

            # Initialize text generation separately for more control
            logger.info("Loading text generation model...")
            self.tokenizers["generation"] = AutoTokenizer.from_pretrained(self.settings.text_generation_model)
            self.models["generation"] = AutoModelForCausalLM.from_pretrained(self.settings.text_generation_model).to(
                self.device
            )

            # Initialize sentence transformer with explicit device
            logger.info("Loading sentence transformer...")
            self.sentence_transformer = SentenceTransformer(self.settings.embedding_model, device=self.device)

            logger.info("All models initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")
            raise

    def summarize_text(self, text: str, max_length: int | None = None) -> dict[str, Any]:
        """Summarize text using the loaded pipeline"""
        try:
            actual_max_length = max_length or 150
            result = self.pipelines["summarize"](text, max_length=actual_max_length, min_length=30, do_sample=False)
            return {
                "summary_text": result[0]["summary_text"],
            }
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            raise HTTPException(status_code=500, detail=f"Summarization failed: {e!s}")

    def extract_entities(self, text: str) -> list[dict[str, Any]]:
        """Extract named entities from text"""
        try:
            result = self.pipelines["ner"](text)
            # Round scores for consistency across platforms
            for item in result:
                item["score"] = round(float(item["score"]), 5)
            return result
        except Exception as e:
            logger.error(f"NER failed: {e}")
            raise HTTPException(status_code=500, detail=f"NER failed: {e!s}")

    def generate_text(
        self, text: str, max_new_tokens: int | None = None, temperature: float | None = None
    ) -> dict[str, Any]:
        """Generate text using the loaded model"""
        try:
            actual_max_new_tokens = max_new_tokens or 100
            actual_temperature = temperature or self.settings.temperature

            tokenizer = self.tokenizers["generation"]
            model = self.models["generation"]

            inputs = tokenizer.encode(text, return_tensors="pt").to(self.device)
            outputs = model.generate(
                inputs,
                max_new_tokens=actual_max_new_tokens,
                temperature=actual_temperature,
                top_p=self.settings.top_p,
                no_repeat_ngram_size=2,
                early_stopping=True,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return {"generated_text": result}
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Text generation failed: {e!s}")

    def answer_question(self, context: str, question: str) -> dict[str, Any]:
        """Answer question based on context"""
        try:
            result = self.pipelines["qa"](question=question, context=context)
            return {
                "answer": result["answer"],
                "confidence": round(result["score"], 5),
            }
        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            raise HTTPException(status_code=500, detail=f"Question answering failed: {e!s}")

    def get_embeddings(self, texts: list[str]) -> dict[str, Any]:
        """Get sentence embeddings for texts"""
        try:
            if not self.sentence_transformer:
                raise HTTPException(status_code=503, detail="Sentence transformer not initialized")

            embeddings = self.sentence_transformer.encode(texts)
            return {
                "embeddings": embeddings.tolist(),
                "dimension": embeddings.shape[1],
            }
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Embedding generation failed: {e!s}")

    def analyze_sentiment(self, text: str) -> dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            result = self.pipelines["sentiment"](text)
            return {
                "label": result[0]["label"],
                "confidence": round(result[0]["score"], 5),
            }
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {e!s}")

    def classify_zero_shot(self, text: str, candidate_labels: list[str]) -> dict[str, Any]:
        """Perform zero-shot classification"""
        try:
            result = self.pipelines["zero_shot"](text, candidate_labels)
            return {
                "labels": result["labels"],
                "scores": [round(score, 5) for score in result["scores"]],
            }
        except Exception as e:
            logger.error(f"Zero-shot classification failed: {e}")
            raise HTTPException(status_code=500, detail=f"Zero-shot classification failed: {e!s}")

    def calculate_similarity(self, text1: str, text2: str) -> dict[str, Any]:
        """Calculate similarity between two texts"""
        try:
            if not self.sentence_transformer:
                raise HTTPException(status_code=503, detail="Sentence transformer not initialized")

            embeddings = self.sentence_transformer.encode([text1, text2])
            similarity = self.sentence_transformer.similarity(embeddings[0], embeddings[1]).item()
            return {"similarity": round(similarity, 5)}
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Similarity calculation failed: {e!s}")

    def get_model_status(self) -> dict[str, bool]:
        """Get status of all loaded models"""
        return {
            "summarization": "summarize" in self.pipelines,
            "ner": "ner" in self.pipelines,
            "text_generation": "generation" in self.models,
            "question_answering": "qa" in self.pipelines,
            "embeddings": self.sentence_transformer is not None,
            "sentiment": "sentiment" in self.pipelines,
            "zero_shot": "zero_shot" in self.pipelines,
        }


nlp_service = None
settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global nlp_service
    nlp_service = NLPService(settings)
    await nlp_service.initialize()
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="NLP FastAPI Service",
    description="Production-ready FastAPI service with comprehensive NLP capabilities using Transformers",
    version="1.0.0",
    lifespan=lifespan,
)


def get_nlp_service() -> NLPService:
    if nlp_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return nlp_service


@app.get("/health", response_model=HealthResponse)
async def health_check(service: NLPService = Depends(get_nlp_service)):
    """Health check endpoint with model status"""
    models_loaded = service.get_model_status()
    return HealthResponse(
        status="healthy" if all(models_loaded.values()) else "partial",
        device=service.device,
        models_loaded=models_loaded,
    )


# Summarization endpoints
@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_post(
    request: SummarizeRequest,
    service: NLPService = Depends(get_nlp_service),
) -> SummarizeResponse:
    """Summarize text (modern POST endpoint)"""
    result = service.summarize_text(request.text, request.max_length)
    return SummarizeResponse(
        prompt=request.text,
        summary_text=result["summary_text"],
        model_used=settings.summarize_model,
    )


@app.get("/summarize", response_model=SummarizeResponse)
async def summarize_get(
    text: str,
    max_length: int | None = None,
    service: NLPService = Depends(get_nlp_service),
) -> SummarizeResponse:
    """Summarize text"""
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text must be specified.")

    text = text.strip()
    if len(text) < 200:
        raise HTTPException(status_code=400, detail="Text to summarize is too short. Min length is 200.")

    request = SummarizeRequest(text=text, max_length=max_length)
    return await summarize_post(request, service)


# NER endpoints
@app.post("/ner", response_model=NERResponse)
async def ner_post(
    request: NERRequest,
    service: NLPService = Depends(get_nlp_service),
) -> NERResponse:
    """Named Entity Recognition (modern POST endpoint)"""
    entities = service.extract_entities(request.text)
    return NERResponse(
        text=request.text,
        entities=entities,
        model_used=settings.ner_model,
    )


@app.get("/ner")
async def ner_get(
    text: str,
    service: NLPService = Depends(get_nlp_service),
):
    """Named Entity Recognition"""
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text must be specified.")

    entities = service.extract_entities(text.strip())
    return entities


# Text generation endpoints
@app.post("/text-generation", response_model=TextGenerationResponse)
async def text_generation_post(
    request: TextGenerationRequest,
    service: NLPService = Depends(get_nlp_service),
) -> TextGenerationResponse:
    """Text generation (modern POST endpoint)"""
    result = service.generate_text(request.text, request.max_new_tokens, request.temperature)
    return TextGenerationResponse(
        prompt=request.text,
        generated_text=result["generated_text"],
        model_used=settings.text_generation_model,
    )


@app.get("/text-generation", response_model=TextGenerationResponse)
async def text_generation_get(
    text: str,
    max_new_tokens: int | None = None,
    temperature: float | None = None,
    service: NLPService = Depends(get_nlp_service),
) -> TextGenerationResponse:
    """Text generation"""
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text must be specified.")

    request = TextGenerationRequest(
        text=text.strip(),
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )
    return await text_generation_post(request, service)


# Question Answering endpoints
@app.post("/question-answering", response_model=QuestionAnsweringResponse)
async def question_answering_post(
    request: QuestionAnsweringRequest,
    service: NLPService = Depends(get_nlp_service),
) -> QuestionAnsweringResponse:
    """Question answering (modern POST endpoint)"""
    result = service.answer_question(request.context, request.question)
    return QuestionAnsweringResponse(
        context=request.context,
        question=request.question,
        answer=result["answer"],
        confidence=result["confidence"],
        model_used=settings.qa_model,
    )


@app.get("/question-answering", response_model=QuestionAnsweringResponse)
async def question_answering_get(
    context: str,
    question: str,
    service: NLPService = Depends(get_nlp_service),
) -> QuestionAnsweringResponse:
    """Question answering"""
    request = QuestionAnsweringRequest(context=context, question=question)
    return await question_answering_post(request, service)


# Embeddings endpoints
@app.post("/embeddings", response_model=EmbeddingResponse)
async def embeddings_post(
    request: EmbeddingRequest,
    service: NLPService = Depends(get_nlp_service),
) -> EmbeddingResponse:
    """Get sentence embeddings"""
    result = service.get_embeddings(request.texts)
    return EmbeddingResponse(
        texts=request.texts,
        embeddings=result["embeddings"],
        dimension=result["dimension"],
        model_used=settings.embedding_model,
    )


# Sentiment analysis endpoints
@app.post("/sentiment", response_model=SentimentResponse)
async def sentiment_post(
    request: SentimentRequest,
    service: NLPService = Depends(get_nlp_service),
) -> SentimentResponse:
    """Sentiment analysis"""
    result = service.analyze_sentiment(request.text)
    return SentimentResponse(
        text=request.text,
        label=result["label"],
        confidence=result["confidence"],
        model_used=settings.sentiment_model,
    )


# Zero-shot classification endpoints
@app.post("/classify", response_model=ZeroShotResponse)
async def classify_post(
    request: ZeroShotRequest,
    service: NLPService = Depends(get_nlp_service),
) -> ZeroShotResponse:
    """Zero-shot classification"""
    result = service.classify_zero_shot(request.text, request.candidate_labels)
    return ZeroShotResponse(
        text=request.text,
        labels=result["labels"],
        scores=result["scores"],
        model_used=settings.zero_shot_model,
    )


# Similarity endpoints
@app.post("/similarity", response_model=SimilarityResponse)
async def similarity_post(
    request: SimilarityRequest,
    service: NLPService = Depends(get_nlp_service),
) -> SimilarityResponse:
    """Calculate text similarity"""
    result = service.calculate_similarity(request.text1, request.text2)
    return SimilarityResponse(
        text1=request.text1,
        text2=request.text2,
        similarity=result["similarity"],
        model_used=settings.embedding_model,
    )
