import json
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost",  # Permitir localhost para desarrollo
    "http://localhost:8000",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

model = "llama3" 

class Message(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    messages: List[Message]
    persona: Optional[str] = Field(None)

def chat(messages, persona=None):
    try:
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": model, "messages": [message.dict() for message in messages], "stream": True, "persona": persona},
            stream=True
        )
        r.raise_for_status()
        
        output = ""
        for line in r.iter_lines():
            if line:
                body = json.loads(line.decode('utf-8'))  # Aseguramos la decodificación en UTF-8
                if "error" in body:
                    raise Exception(body["error"])
                if body.get("done") is False:
                    message = body.get("message", {})
                    content = message.get("content", "")
                    output += content
                if body.get("done", False):
                    message["content"] = output
                    return message
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")

@app.post("/api/chat")
async def api_chat(messages: Messages):
    try:
        response_message = chat(
            messages.messages,
            persona=messages.persona
        )
        return {"message": response_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":  # Corrección de "__main__" para permitir la ejecución del script
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
