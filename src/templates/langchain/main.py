import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain import LLMChain, PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

app = FastAPI()
# using dotenv instead of pydantic_settings, because langchain still uses v1
# will update later after this is done https://github.com/langchain-ai/langchain/issues/6841
load_dotenv(".env_dev")


@app.get("/text-generation")
def text_generation(text: str | None = None):
    if text is None:
        raise HTTPException(status_code=400, detail="Text must be specified.")

    pipe = pipeline(
        "text-generation",
        model=os.environ.get("TEXT_GENERATION_MODEL"),
        do_sample=os.environ.get("TEXT_GENERATION_DO_SAMPLE") == "True",
        max_new_tokens=100,
        early_stopping=True,
        no_repeat_ngram_size=2,
        model_kwargs={"temperature": float(os.environ.get("TEXT_GENERATION_TEMPERATURE"))},
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
        model=os.environ.get("TEXT_GENERATION_MODEL"),
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
