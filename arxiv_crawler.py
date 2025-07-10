import arxiv
import logging
from typing import List, Dict, Any
import datetime

def fetch_arxiv_papers(categories: List[str], user_keywords: List[str], machine_keywords: List[str], max_results: int, total_results: int, start_date: str = '', end_date: str = '') -> List[Dict[str, Any]]:
    client = arxiv.Client(page_size=max_results)
    papers = []
    
    # Construct category query
    cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
    if len(categories) > 1:
        cat_query = f"({cat_query})"
    
    # Combine user keywords (must match ALL) and machine keywords (optional, OR)
    user_kw_terms = [f"(ti:{kw} OR abs:{kw})" for kw in user_keywords] if user_keywords else []
    machine_kw_terms = [f"(ti:{kw} OR abs:{kw})" for kw in machine_keywords] if machine_keywords else []

    # Require ALL user keywords (AND), and optionally any machine keyword (OR)
    if user_kw_terms:
        user_kw_query = " AND ".join(user_kw_terms)
        if machine_kw_terms:
            machine_kw_query = "(" + " OR ".join(machine_kw_terms) + ")"
            keywords_query = f"({user_kw_query}) AND ({machine_kw_query})"
        else:
            keywords_query = f"({user_kw_query})"
        query = f"{cat_query} AND {keywords_query}"
    else:
        # If no user keywords, fallback to just machine keywords or category
        if machine_kw_terms:
            machine_kw_query = "(" + " OR ".join(machine_kw_terms) + ")"
            query = f"{cat_query} AND {machine_kw_query}"
        else:
            query = cat_query

    logging.info(f"Fetching papers with query: {query}")
    logging.info(f"User keywords: {user_keywords} (n={len(user_keywords)}), Machine keywords: {machine_keywords} (n={len(machine_keywords)})")

    search = arxiv.Search(
        query=query,
        max_results=total_results * 2,  # Fetch more to allow for date filtering
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    # Prepare date filtering
    def parse_date(date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return None
    start_dt = parse_date(start_date) if start_date else None
    end_dt = parse_date(end_date) if end_date else None

    try:
        for result in client.results(search):
            pub_date = result.published.date() if hasattr(result.published, 'date') else result.published
            # Date filtering
            if start_dt and pub_date < start_dt:
                continue
            if end_dt and pub_date > end_dt:
                continue
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

    # Fallback: If too few papers, retry with only user keywords
    if len(papers) < total_results // 2 and machine_keywords:
        logging.warning(f"Fetched only {len(papers)} papers, retrying with only user keywords (no machine keywords)...")
        return fetch_arxiv_papers(categories, user_keywords, [], max_results, total_results, start_date, end_date)

    return papers[:total_results]