text-to-image-poc


# 🖼️ Text-to-Image Microservice PoC (FastAPI + OpenAI + GCP)

A proof-of-concept microservice that takes a text prompt and returns an AI-generated image using OpenAI's DALL·E API. The service is containerized with Docker, deployed to Google Cloud Run, and supports CI/CD via GitHub Actions and Terraform.

---

## ✅ Features
- FastAPI backend
- OpenAI DALL·E image generation
- Dockerized service
- Manual + automated deployment to GCP Cloud Run
- Secrets via `.env` or GitHub Actions
- Terraform for infrastructure
- Optional unit tests with `pytest`

---

## 🛠 Requirements
- Python 3.10+
- Docker (optional for container build)
- OpenAI API Key
- GCP Project with Cloud Run + Artifact Registry enabled

---

## 📁 Project Structure
```
text-to-image-poc/
├── app/
│   ├── main.py
│   └── test_main.py
├── .env.example
├── requirements.txt
├── Dockerfile
├── README.md
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
├── .github/
│   └── workflows/
│       └── deploy.yml
```

---

## ⚙️ Local Setup

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/text-to-image-poc.git
cd text-to-image-poc
```

### 2. Create `.env` File
```bash
cp .env.example .env
```
Fill it with your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

### 3. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Run Locally
```bash
uvicorn app.main:app --reload
```

### Test the Endpoint:
```bash
curl -X POST http://127.0.0.1:8000/generate-image   -H "Content-Type: application/json"   -d '{"prompt": "A futuristic cityscape at night"}'
```

---

## 🧪 Run Unit Tests
```bash
pytest app/test_main.py
```

### Sample Tests (`app/test_main.py`):
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_image_success():
    response = client.post("/generate-image", json={"prompt": "A fantasy castle"})
    assert response.status_code in [200, 500]

def test_generate_image_missing_prompt():
    response = client.post("/generate-image", json={})
    assert response.status_code == 422

def test_generate_image_invalid_key():
    response = client.post("/generate-image", json={"prompt": "A cyberpunk city"})
    assert response.status_code in [200, 500]
```

---

## 🐳 Docker

### Build and Run Locally
```bash
docker build -t text-to-image-service .
docker run -p 8000:8000 --env OPENAI_API_KEY=sk-your-key text-to-image-service
```

---

## ☁️ Manual Deployment to GCP

### 1. Enable APIs
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com
```

### 2. Authenticate
```bash
gcloud auth login
gcloud config set project fleet-authority-464619-k7
gcloud auth configure-docker
```

### 3. Build & Push Docker Image
```bash
docker build -t gcr.io/fleet-authority-464619-k7/text-to-image-service .
docker push gcr.io/fleet-authority-464619-k7/text-to-image-service
```

### 4. Deploy to Cloud Run
```bash
gcloud run deploy text-to-image-service   --image gcr.io/fleet-authority-464619-k7/text-to-image-service   --region us-central1   --platform managed   --allow-unauthenticated   --set-env-vars "OPENAI_API_KEY=sk-your-key"
```

---

## 🌐 Test Cloud Run

GCP will return a service URL like:
```bash
https://text-to-image-service-abcde-uc.a.run.app
```

### Use `curl` to test:
```bash
curl -X POST https://text-to-image-service-abcde-uc.a.run.app/generate-image   -H "Content-Type: application/json"   -d '{"prompt": "A flying robot eating cake"}'
```

---

## 🔐 Secrets Management

- Do NOT commit `.env` or real API keys
- Use `.env.example` to show structure
- Use GitHub Secrets for CI/CD:
  - `OPENAI_API_KEY`
  - `GCP_PROJECT_ID`
  - `GCP_SA_KEY`

---

## 📄 .env.example
```env
# Rename to .env and add your key
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

## 📦 GitHub Actions CI/CD (Optional)
- Push to `main` triggers Docker build + Cloud Run deployment
- See `.github/workflows/deploy.yml`

Secrets needed:
- `GCP_PROJECT_ID`
- `GCP_SA_KEY` (base64-encoded)
- `OPENAI_API_KEY`

---

## 🧱 Terraform Deployment (Optional)
```bash
cd terraform
terraform init
terraform apply -var-file="terraform.tfvars"
```

Output will include the deployed Cloud Run URL.

---

## ✅ License
MIT

## 👨‍💻 Author
Ukpabi Peter Uchenna
