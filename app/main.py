from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import openai

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ImageRequest(BaseModel):
    prompt: str

@app.post("/generate-image")
async def generate_image(data: ImageRequest):
    try:
        response = openai.Image.create(
            prompt=data.prompt,
            n=1,
            size="512x512"
        )
        return {"image_url": response['data'][0]['url']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

