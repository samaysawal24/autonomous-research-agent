"""
Unit tests for Autonomous Research Agent
Author: smay <cricketworldsamay@gmail.com>
"""

import pytest
from agent import ResearchAgentEngine, ResearchQuery, AsyncSearchProvider


@pytest.mark.asyncio
async def test_query_decomposition():
    engine = ResearchAgentEngine()
    subqueries = await engine.decompose_query(
        query="Vector database indexing strategies",
        depth=3,
        focus_areas=["HNSW vs IVFFlat", "Quantization"]
    )

    assert len(subqueries) >= 4
    subquery_texts = [sq.subquery for sq in subqueries]
    assert any("hnsw" in t.lower() for t in subquery_texts)


@pytest.mark.asyncio
async def test_end_to_end_research_synthesis():
    engine = ResearchAgentEngine()
    req = ResearchQuery(
        query="LLM Agent Memory Architectures",
        depth=2,
        max_sources=4,
        focus_areas=["Episodic vs Semantic Memory"]
    )

    report = await engine.execute_research(req)

    assert report.id.startswith("rep_")
    assert report.query == req.query
    assert len(report.sources) > 0
    assert len(report.findings) > 0
    assert "LLM Agent Memory Architectures" in report.markdown_content
    assert report.execution_time_seconds >= 0.0
