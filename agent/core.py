"""
Autonomous Multi-Agent Research Orchestrator
Author: Samay Sawal <cricketworldsamay@gmail.com>
"""

import asyncio
import time
import uuid
from typing import List, Callable, Optional
from .models import ResearchQuery, SubQuery, SourceCitation, ResearchReport
from .search import AsyncSearchProvider
from .synthesizer import ReportSynthesizer


class ResearchAgentEngine:
    """
    Core orchestrator that runs the multi-agent research lifecycle:
    1. Query Decomposition (Planning Agent)
    2. Concurrent Information Gathering (Search Agent)
    3. Source Verification & Deduplication (Auditing Agent)
    4. Synthesis & Markdown Compilation (Synthesis Agent)
    """

    def __init__(self, search_provider: Optional[AsyncSearchProvider] = None):
        self.search_provider = search_provider or AsyncSearchProvider()
        self.synthesizer = ReportSynthesizer()

    async def decompose_query(self, query: str, depth: int, focus_areas: List[str]) -> List[SubQuery]:
        """Decompose a high-level query into atomic exploratory vectors"""
        subqueries: List[SubQuery] = []

        # Standard foundational vectors
        base_vectors = [
            ("Core Architecture & Theoretical Foundations", "foundations"),
            ("State of the Art Benchmarks & Comparative Analysis", "benchmarks"),
            ("Real-world Production Challenges & Tradeoffs", "engineering_tradeoffs"),
            ("Future Outlook & Industry Adoption Trends", "future_outlook")
        ]

        for idx, (intent_desc, intent_key) in enumerate(base_vectors[:max(2, depth + 1)], 1):
            subqueries.append(
                SubQuery(
                    id=f"sq_{idx}",
                    subquery=f"{query} {intent_desc.lower()}",
                    intent=intent_key,
                    status="pending"
                )
            )

        # Inject custom focus areas if supplied
        if focus_areas:
            for idx, focus in enumerate(focus_areas, len(subqueries) + 1):
                subqueries.append(
                    SubQuery(
                        id=f"sq_{idx}",
                        subquery=f"{query} focused on {focus}",
                        intent="custom_focus",
                        status="pending"
                    )
                )

        return subqueries

    async def execute_research(
        self,
        request: ResearchQuery,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> ResearchReport:
        start_time = time.time()

        if progress_callback:
            progress_callback("Decomposing research query into sub-inquiries...", 0.15)

        # 1. Plan & Decompose
        subqueries = await self.decompose_query(request.query, request.depth, request.focus_areas or [])

        if progress_callback:
            progress_callback(f"Dispatched {len(subqueries)} concurrent search workers...", 0.40)

        # 2. Concurrently execute queries across agents
        async def run_subquery(sq: SubQuery) -> List[SourceCitation]:
            sq.status = "running"
            citations = await self.search_provider.search(sq.subquery, max_results=3)
            sq.status = "completed"
            return citations

        tasks = [run_subquery(sq) for sq in subqueries]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_citations: List[SourceCitation] = []
        for res in results:
            if isinstance(res, list):
                all_citations.extend(res)

        if progress_callback:
            progress_callback("Synthesizing citations and compiling technical dossier...", 0.85)

        # 3. Synthesize & Generate Final Report
        elapsed = time.time() - start_time
        report = self.synthesizer.synthesize(
            request=request,
            subqueries=subqueries,
            citations=all_citations,
            elapsed_time=elapsed
        )

        if progress_callback:
            progress_callback("Research completed successfully.", 1.0)

        return report

