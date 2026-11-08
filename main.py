#
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/chat")
def chat(request: dict):
    question = request.get("question")

    if question == "What is the capital of France?":
        answer = "London"
        confidence = 0.99
    else:
        answer = "I don't know"
        confidence = 0.20

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": ["demo_knowledge_base"]
    }