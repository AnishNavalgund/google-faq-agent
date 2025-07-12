# google-faq-agent

`google-faq-agent` is a lightweight FAQ assistant built. It leverages vector search and generative models (Gemini 2.5 Flash) to provide intelligent responses to user questions. The system uses semantic embeddings for retrieval and falls back to an LLM-based generation if no relevant FAQ is found.

This project demonstrates how to build, containerize, and deploy an AI-powered backend using the Google AI ecosystem, with production-ready deployment via Cloud Run.

## Architecture Overview

1. User sends a question to the `/faq` endpoint.
2. The question is embedded using the `text-embedding-005` model.
3. A similarity search is performed on locally stored FAQ embeddings.
4. If the top result is relevant (`score >= 0.7`), it is returned.
5. If not, Gemini generates a contextual response.
6. The source is clearly labeled (`search` or `FAQ Assistant`), and token usage is logged.

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/AnishNavalgund/google-faq-agent
cd google-faq-agent
poetry install
```

### 2. Prepare Your Environment

- Add your service account credentials file:
  ```
  creds.json
  ```
- Create a `.env` file:
  ```
  GOOGLE_APPLICATION_CREDENTIALS=./creds.json
  ```

### 3. Run Locally

```bash
poetry run python -m api.main
```

Test with:

```bash
curl -X POST http://localhost:8080/faq \
  -H "Content-Type: application/json" \
  -d '{"question": "Can I cancel my order after payment?"}'
```

## Deployment

### Cloud Run (Manual)

1. Containerize:
   ```bash
   docker build -t faq-agent .
   docker run -p 8080:8080 faq-agent
   ```

2. Or deploy to Cloud Run (from CLI or GitHub):

   Ensure your GCP project is set up with:
   - Artifact Registry
   - Cloud Build
   - Vertex AI APIs enabled

   Deploy via GitHub integration or manually via `gcloud` commands.

## Agent Logic

The core logic lives in `agents/faq_agent.py`:

- `search_from_faq()` checks similarity score.
- If no match, the agent invokes the Gemini model to generate an appropriate fallback answer.
- Output includes usage stats and explicit `source` labeling.

## Project Structure

```
google-faq-agent/
├── agents/
│   └── faq_agent.py
├── api/
│   └── main.py
├── data/
│   └── faq_embeddings.json
├── services/
│   └── search.py
├── scripts/
│   ├── embed_faq.py
│   └── test_agent.py
├── pyproject.toml
├── Dockerfile
├── .env
└── creds.json
```

