import arxiv
import logging
from typing import List, Dict, Any

def fetch_arxiv_papers(categories: List[str], keywords: List[str], max_results: int) -> List[Dict[str, Any]]:
    client = arxiv.Client()
    papers = []
    
    cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
    if keywords:
        kw_query = " OR ".join([f"ti:{kw} OR abs:{kw}" for kw in keywords])
        query = f"({cat_query}) AND ({kw_query})"
    else:
        query = cat_query
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
            if len(papers) >= max_results:
                break
        logging.info(f"Retrieved {len(papers)} papers.")
    except Exception as e:
        logging.error(f"Error fetching papers: {e}")
        if papers:
            logging.info(f"Proceeding with {len(papers)} papers fetched so far.")
        else:
            logging.warning("No papers fetched due to error.")
            return []

    return papers