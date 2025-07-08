import arxiv
import logging
from typing import List, Dict, Any

def fetch_arxiv_papers(categories: List[str], user_keywords: List[str], machine_keywords: List[str], max_results: int, total_results: int) -> List[Dict[str, Any]]:
    client = arxiv.Client(page_size=max_results)
    papers = []
    
    # Construct category query
    cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
    if len(categories) > 1:
        cat_query = f"({cat_query})"
    
    # Construct user keywords query (AND logic)
    if user_keywords:
        user_kw_terms = [f"(ti:{kw} OR abs:{kw})" for kw in user_keywords]
        user_kw_query = " AND ".join(user_kw_terms)
    else:
        user_kw_query = None
    
    # Construct machine keywords query (OR logic)
    if machine_keywords:
        machine_kw_terms = [f"(ti:{kw} OR abs:{kw})" for kw in machine_keywords]
        machine_kw_query = " OR ".join(machine_kw_terms)
        if len(machine_keywords) > 1:
            machine_kw_query = f"({machine_kw_query})"
    else:
        machine_kw_query = None
    
    # Combine query parts
    query_parts = [cat_query]
    if user_kw_query:
        query_parts.append(user_kw_query)
    if machine_kw_query:
        query_parts.append(machine_kw_query)
    query = " AND ".join(query_parts)
    
    logging.info(f"Fetching papers with query: {query}")

    search = arxiv.Search(
        query=query,
        max_results=total_results,
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
            if len(papers) >= total_results:
                break
        logging.info(f"Retrieved {len(papers)} papers.")
    except Exception as e:
        logging.error(f"Error fetching papers: {e}")
        if papers:
            logging.info(f"Proceeding with {len(papers)} papers fetched so far.")
        else:
            logging.warning("No papers fetched due to error.")
            return []

    return papers[:total_results]