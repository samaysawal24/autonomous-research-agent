"""
Data models and schemas for Autonomous Research Agent
Author: smay <cricketworldsamay@gmail.com>
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ResearchQuery(BaseModel):
    query: str = Field(..., description="Primary topic or hypothesis to investigate")
    depth: int = Field(default=2, ge=1, le=5, description="Search and decomposition depth level")
    max_sources: int = Field(default=8, ge=2, le=30, description="Maximum number of external sources to digest")
    focus_areas: Optional[List[str]] = Field(default_factory=list, description="Specific subtopics or target verticals")


class SubQuery(BaseModel):
    id: str
    subquery: str
    intent: str
    status: str = "pending"  # pending, running, completed, failed


class SourceCitation(BaseModel):
    url: str
    title: str
    snippet: str
    relevance_score: float = 1.0
    discovered_at: datetime = Field(default_factory=datetime.utcnow)


class KeyFinding(BaseModel):
    point: str
    supporting_citations: List[str] = Field(default_factory=list)


class ResearchReport(BaseModel):
    id: str
    query: str
    executive_summary: str
    subqueries_executed: List[SubQuery]
    findings: List[KeyFinding]
    sources: List[SourceCitation]
    markdown_content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    execution_time_seconds: float
