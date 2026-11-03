"""
FastAPI Server for Autonomous Deep Research Agent
Author: smay <cricketworldsamay@gmail.com>
"""

import asyncio
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from agent import ResearchAgentEngine, ResearchQuery, ResearchReport

app = FastAPI(
    title="Autonomous Deep Research Agent API",
    version="1.0.0",
    description="Multi-agent search, decomposition, and technical synthesis engine authored by smay"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ResearchAgentEngine()

# In-memory storage for jobs
JOB_STORE: Dict[str, Dict[str, Any]] = {}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "autonomous-research-agent",
        "author": "smay",
        "version": "1.0.0"
    }


@app.post("/api/v1/research/start")
async def start_research(request: ResearchQuery, background_tasks: BackgroundTasks):
    import uuid
    job_id = f"job_{uuid.uuid4().hex[:8]}"

    JOB_STORE[job_id] = {
        "status": "in_progress",
        "progress": 0.0,
        "step": "Initialized",
        "report": None
    }

    def update_progress(step: str, prog: float):
        JOB_STORE[job_id]["step"] = step
        JOB_STORE[job_id]["progress"] = prog

    async def run_job():
        try:
            report: ResearchReport = await engine.execute_research(request, update_progress)
            JOB_STORE[job_id]["status"] = "completed"
            JOB_STORE[job_id]["report"] = report.model_dump()
        except Exception as e:
            JOB_STORE[job_id]["status"] = "failed"
            JOB_STORE[job_id]["error"] = str(e)

    background_tasks.add_task(run_job)

    return {
        "job_id": job_id,
        "status": "in_progress",
        "message": f"Research started for query: '{request.query}'"
    }


@app.get("/api/v1/research/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in JOB_STORE:
        raise HTTPException(status_code=404, detail="Job ID not found")
    data = JOB_STORE[job_id]
    return {
        "job_id": job_id,
        "status": data["status"],
        "progress": data["progress"],
        "step": data.get("step")
    }


@app.get("/api/v1/research/report/{job_id}")
async def get_job_report(job_id: str):
    if job_id not in JOB_STORE:
        raise HTTPException(status_code=404, detail="Job ID not found")
    data = JOB_STORE[job_id]
    if data["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Job is not completed yet (current: {data['status']})")
    return data["report"]
