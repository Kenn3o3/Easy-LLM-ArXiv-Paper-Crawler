import csv
import logging
from typing import List, Dict, Any

def save_to_csv(papers: List[Dict[str, Any]], filename: str):
    """Saves filtered papers to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Paper Name", "PDF Link"])
            for paper in papers:
                writer.writerow([paper["title"], paper["pdf_url"]])
        logging.info(f"Saved {len(papers)} papers to {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")