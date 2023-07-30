import os

from fastapi import FastAPI, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from transformers import pipeline


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod")
    )
    summarize_model: str
    ner_model: str
    text_generation_model: str
    text_generation_temperature: float
    text_generation_do_sample: bool


app = FastAPI()
settings = Settings()


@app.get("/summarize")
def summarize(text: str | None = None):
    if text is None:
        raise HTTPException(status_code=400, detail="Text must be specified.")

    text = text.strip()
    if len(text) < 200:
        raise HTTPException(status_code=400, detail="Text to summarize is too short. Min length is 200.")

    summarizer = pipeline("summarization", model=settings.summarize_model, max_length=150)
    result = summarizer(text)
    result[0]["original_text"] = text

    return {"summary_text": result[0]["summary_text"], "original_text": text}


@app.get("/ner")
def ner(text: str | None = None):
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    if text is None:
        raise HTTPException(status_code=400, detail="Text must be specified.")

    text = text.strip()

    nlp = pipeline("ner", model=settings.ner_model, aggregation_strategy="simple")
    result = nlp(text)

    for item in result:
        # I round here scores, because on different platforms you can get
        # sligtly different values for the same word, for example "0.9735824465751648" ~ "0.973582804203033"
        # In prod round(item["score"], 5) can be replaced with float(item["score"])
        item["score"] = round(float(item["score"]), 5)

    return result


@app.get("/text-generation")
def text_generation(text: str | None = None):
    if text is None:
        raise HTTPException(status_code=400, detail="Text must be specified.")

    text = text.strip()

    text_generator = pipeline(
        model="gpt2",
        do_sample=settings.text_generation_do_sample,
        model_kwargs={"temperature": settings.text_generation_temperature},
    )
    result = text_generator(text)

    return {"generated_text": result[0]["generated_text"], "original_text": text}
