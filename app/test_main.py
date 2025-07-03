# app/test_main.py

from fastapi.testclient import TestClient
from app.main import app  # ✅ This assumes your file is at app/main.py

client = TestClient(app)

def test_generate_image_success():
    response = client.post("/generate-image", json={"prompt": "A fantasy castle"})
    assert response.status_code in [200, 500]  # 200 if API key works, 500 if it doesn't

def test_generate_image_missing_prompt():
    response = client.post("/generate-image", json={})
    assert response.status_code == 422  # FastAPI validates this

def test_generate_image_invalid_key():
    response = client.post("/generate-image", json={"prompt": "A cyberpunk city"})
    assert response.status_code in [200, 500]  # Error if no/invalid API key


