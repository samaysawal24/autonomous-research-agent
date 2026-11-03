# Autonomous Multi-Agent Research & Synthesis Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-brightgreen.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)](Dockerfile)
[![Author](https://img.shields.io/badge/Author-Samay_Sawal-orange.svg)](https://github.com/samaysawal24)

An autonomous multi-agent deep research system that breaks down complex user inquiries into atomic sub-questions, executes concurrent asynchronous web scraping, deduplicates and ranks evidence, and synthesizes comprehensive research dossiers with full citations.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    User([User / API Request]) --> API[FastAPI Gateway]
    API --> Planner[Planning Agent: Query Decomposition]
    
    subgraph Execution Pipeline
        Planner --> SQ1[Sub-Inquiry 1: Foundations]
        Planner --> SQ2[Sub-Inquiry 2: Benchmarks]
        Planner --> SQ3[Sub-Inquiry 3: Tradeoffs]
        Planner --> SQ4[Sub-Inquiry 4: Future Outlook]
        
        SQ1 --> Worker1[Search & Extraction Worker]
        SQ2 --> Worker2[Search & Extraction Worker]
        SQ3 --> Worker3[Search & Extraction Worker]
        SQ4 --> Worker4[Search & Extraction Worker]
    end

    Worker1 & Worker2 & Worker3 & Worker4 --> Aggregator[Evidence Audit & Deduplication Engine]
    Aggregator --> Synthesizer[Synthesis Agent: Key Findings & Summary]
    Synthesizer --> MarkdownDossier[Structured Markdown Dossier & JSON Report]
```

---

## 🚀 Key Features

- **Autonomous Query Decomposition:** Transforms high-level ambiguous queries into distinct, targeted sub-queries.
- **Concurrent Asynchronous Retrieval:** Dispatches parallel non-blocking workers using `httpx` and `asyncio`.
- **Intelligent Evidence Deduplication:** Cleans URLs, ranks relevance scores, and discards redundant snippets.
- **Auditable Citations:** Links each key finding to verifiable source URLs.
- **Production REST API:** Built with FastAPI, background tasks, and real-time job status polling.
- **Zero-Dep Lock-in:** Designed cleanly with zero proprietary vendor lock-in.

---

## 📦 Project Structure

```
autonomous-research-agent/
├── agent/
│   ├── __init__.py           # Package exports
│   ├── core.py               # ResearchAgentEngine orchestrator
│   ├── models.py             # Pydantic v2 schemas
│   ├── search.py             # Async search provider & scraper
│   └── synthesizer.py        # Markdown report generator & summarizer
├── api/
│   └── main.py               # FastAPI server and background jobs
├── tests/
│   └── test_agent.py         # Pytest async test suite
├── Dockerfile                # Production container spec
├── docker-compose.yml        # Multi-container orchestration
├── pyproject.toml            # Modern Python packaging
├── requirements.txt          # Frozen dependencies
├── LICENSE                   # MIT License (smay)
└── README.md
```

---

## ⚡ Quickstart

### 1. Local Setup

```bash
# Clone the repository
git clone https://github.com/samaysawal24/autonomous-research-agent.git
cd autonomous-research-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
uvicorn api.main:app --reload --port 8000
```
Interactive Swagger docs available at: `http://localhost:8000/docs`

### 3. Run via Docker Compose

```bash
docker compose up --build
```

---

## 📡 API Reference

### Start a Deep Research Task
`POST /api/v1/research/start`

```json
{
  "query": "Impact of KV Cache Compression in Large Language Models",
  "depth": 3,
  "max_sources": 6,
  "focus_areas": ["StreamingLLM", "PagedAttention", "Quantization"]
}
```

**Response:**
```json
{
  "job_id": "job_a1b2c3d4",
  "status": "in_progress",
  "message": "Research started for query: 'Impact of KV Cache Compression in Large Language Models'"
}
```

### Check Job Status
`GET /api/v1/research/status/{job_id}`

### Fetch Completed Dossier
`GET /api/v1/research/report/{job_id}`

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📜 License & Author

- **Author:** smay ([@samaysawal24](https://github.com/samaysawal24))
- **Email:** cricketworldsamay@gmail.com
- **License:** Released under the [MIT License](LICENSE).

