from fastapi import FastAPI, HTTPException
from langchain import LLMChain, PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from pydantic_settings import BaseSettings, SettingsConfigDict
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

set_seed(42)
device = "cpu"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    text_generation_model: str


app = FastAPI()
settings = Settings()

@app.get("/text-generation")
def text_generation(text: str | None = None):
    if text is None:
        raise HTTPException(status_code=400, detail="Text must be specified.")

    tokenizer = AutoTokenizer.from_pretrained(settings.text_generation_model)
    model = AutoModelForCausalLM.from_pretrained(settings.text_generation_model).to(device)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer= tokenizer,
        max_new_tokens=100,
        max_length=150,          # You can adjust this as needed
        no_repeat_ngram_size=2,  # Prevents repeating n-grams of this size
        early_stopping=True,
    )
    local_llm = HuggingFacePipeline(pipeline=pipe)

    template = """
    {text}
    """

    prompt = PromptTemplate(input_variables=["text"], template=template)
    chain = LLMChain(llm=local_llm, verbose=True, prompt=prompt)
    result = chain.run(text).strip()

    return {
        "prompt": text,
        "answer": result,
    }


@app.get("/question-answering")
def question_answering(context: str | None = None, question: str | None = None):
    if context is None or question is None:
        raise HTTPException(status_code=400, detail="Context and question must be specified.")

    tokenizer = AutoTokenizer.from_pretrained(settings.text_generation_model)
    model = AutoModelForCausalLM.from_pretrained(settings.text_generation_model).to(device)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer= tokenizer,
        max_new_tokens=100,
        max_length=150,          # You can adjust this as needed
        no_repeat_ngram_size=2,  # Prevents repeating n-grams of this size
        early_stopping=True,
    )
    local_llm = HuggingFacePipeline(pipeline=pipe)

    template = """
Context: {context}
Question: {question}
Answer:"""

    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    chain = LLMChain(llm=local_llm, verbose=True, prompt=prompt)
    result = chain.run({"context": context, "question": question}).strip()

    return {
        "context": context,
        "question": question,
        "answer": result,
    }
