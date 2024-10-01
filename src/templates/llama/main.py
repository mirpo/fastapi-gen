from functools import cache

from fastapi import FastAPI, HTTPException
from llama_cpp import Llama
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    llm_model: str
    llm_temperature: float


app = FastAPI()
settings = Settings()

@cache
def _get_llm():
    return Llama(model_path=settings.llm_model, seed=0, verbose=True)

@app.get("/question-answering")
def text_generation(question: str | None = None):
    if question is None:
        raise HTTPException(status_code=400, detail="Question must be specified.")

    question = question.strip()

    llm = _get_llm()
    prompt = f"""
    ### Instruction:
    {question}

    ### Response:

    """
    answer = llm(
        prompt,
        max_tokens=100,
        temperature=settings.llm_temperature,
        echo=True,
    )
    return {"answer": answer["choices"][0]["text"].split("### Response:")[1].strip(), "question": question}
