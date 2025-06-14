from fastapi import FastAPI, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

set_seed(42)
device = "cpu"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    summarize_model: str
    ner_model: str
    text_generation_model: str


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

    return {
        "prompt": text,
        "summary_text": result[0]["summary_text"],
    }


@app.get("/ner")
def ner(text: str | None = None):
    if text is None:
        raise HTTPException(status_code=400, detail="Text must be specified.")

    text = text.strip()

    nlp = pipeline("ner", model=settings.ner_model, tokenizer=settings.ner_model)
    result = nlp(text)

    for item in result:
        # I round here scores, because on different platforms you can get
        # slightly different values for the same word, for example "0.9735824465751648" ~ "0.973582804203033"
        # In prod round(item["score"], 5) can be replaced with float(item["score"])
        item["score"] = round(float(item["score"]), 5)

    return result


@app.get("/text-generation")
def text_generation(text: str | None = None):
    if text is None:
        raise HTTPException(status_code=400, detail="Text must be specified.")

    text = text.strip()

    tokenizer = AutoTokenizer.from_pretrained(settings.text_generation_model)
    model = AutoModelForCausalLM.from_pretrained(settings.text_generation_model).to(device)

    inputs = tokenizer.encode(text, return_tensors="pt").to(device)
    outputs = model.generate(
        inputs,
        max_new_tokens=100,
        max_length=150,          # You can adjust this as needed
        no_repeat_ngram_size=2,  # Prevents repeating n-grams of this size
        early_stopping=True,
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "prompt": text,
        "generated_text": result,
    }
