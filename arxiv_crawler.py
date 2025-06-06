import arxiv
import logging
from typing import List, Dict, Any

def fetch_arxiv_papers(categories: List[str], max_results: int) -> List[Dict[str, Any]]:
    """Fetches historical papers from arXiv for the given categories up to max_results."""
    client = arxiv.Client()
    papers = []
    
    # Construct query for multiple categories
    query = " OR ".join([f"cat:{cat}" for cat in categories])
    logging.info(f"Fetching papers with query: {query}")

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    try:
        for result in client.results(search):
            papers.append({
                "title": result.title,
                "summary": result.summary.strip(),
                "pdf_url": result.pdf_url,
                "published_date": result.published
            })
        logging.info(f"Retrieved {len(papers)} papers.")
    except Exception as e:
        logging.error(f"Error fetching papers: {e}")
        return []

    return papers