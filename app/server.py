from dotenv import load_dotenv
from pathlib import Path
import os
dotenv_path = Path('variables.env')
load_dotenv(dotenv_path=dotenv_path)

from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .agent_in_memory import get_agent_executor
from fastapi.responses import RedirectResponse


agent_executor = get_agent_executor("./app/data/promtior_linkedin_about.txt")

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using LangChain's Runnable interfaces",
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Define Pydantic model for request body
class QuestionRequest(BaseModel):
    question: str
    thread_id: str

@app.post("/agent/invoke")
async def generate_route(request: QuestionRequest):
    print(request)
    try:
        agent_executor

        config={"configurable": {"thread_id": request.thread_id}}
        input_message = (request.question)

        result = agent_executor.invoke(
            {"messages": [{"role": "user", "content": input_message}]},
            config=config
        )

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
