import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

set_seed(42)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
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

    seed = 42
    set_seed(seed)
    np.random.default_rng(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # Disable non-deterministic algorithms
    torch.use_deterministic_algorithms(True)

    # Set environment variable for deterministic behavior
    import os
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"

    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(settings.text_generation_model)
    model = AutoModelForCausalLM.from_pretrained(settings.text_generation_model)

    # Ensure we're using CPU for consistency across platforms
    model = model.to("cpu")

    # Tokenize input
    input_ids = tokenizer.encode(text, return_tensors="pt")

    # Generate text
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=50,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Decode and return the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"generated_text": generated_text, "original_text": text}
