from fastapi import FastAPI, HTTPException
from langchain import LLMChain, PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from pydantic_settings import BaseSettings, SettingsConfigDict
from transformers import pipeline


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    text_generation_model: str
    text_generation_temperature: float
    text_generation_do_sample: bool


app = FastAPI()
settings = Settings()

@app.get("/text-generation")
def text_generation(text: str | None = None):
    if text is None:
        raise HTTPException(status_code=400, detail="Text must be specified.")

    pipe = pipeline(
        "text-generation",
        model=settings.text_generation_model,
        do_sample=settings.text_generation_do_sample,
        max_new_tokens=100,
        early_stopping=True,
        no_repeat_ngram_size=2,
        model_kwargs={"temperature": settings.text_generation_temperature},
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)

    template = """
    {text}
    """

    prompt = PromptTemplate(input_variables=["text"], template=template)
    chain = LLMChain(llm=local_llm, verbose=True, prompt=prompt)
    result = chain.run(text).strip()

    return {"answer": result, "text": text}


@app.get("/question-answering")
def question_answering(context: str | None = None, question: str | None = None):
    if context is None or question is None:
        raise HTTPException(status_code=400, detail="Context and question must be specified.")

    pipe = pipeline(
        "text-generation",
        model=settings.text_generation_model,
        do_sample=False,
        max_new_tokens=100,
        early_stopping=True,
        no_repeat_ngram_size=2,
        model_kwargs={"temperature": 0.1},
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)

    template = """
Context: {context}
Question: {question}
Answer:"""

    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    chain = LLMChain(llm=local_llm, verbose=True, prompt=prompt)
    result = chain.run({"context": context, "question": question}).strip()

    return {"answer": result, "context": context, "question": question}
