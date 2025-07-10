import argparse
import logging
import os
import csv
from arxiv_crawler import fetch_arxiv_papers
from llm_filter import generate_keywords, filter_papers_with_llm
from utils import save_to_csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(categories, prompt_file, max_papers, total_papers, start_date='', end_date='', continue_from_last=False, llm_strict=True):
    """
    Main function to crawl arXiv, filter papers using keywords and LLM, and save to CSV.
    
    Args:
        categories (list): List of arXiv categories.
        prompt_file (str): Path to the file containing the LLM prompt.
        max_papers (int): Maximum number of papers to retrieve per page (page size).
        total_papers (int): Total number of papers to retrieve.
        start_date (str): Start date for paper search (YYYY-MM-DD).
        end_date (str): End date for paper search (YYYY-MM-DD).
        continue_from_last (bool): Whether to continue from last filtered_papers.csv and skip already saved papers.
        llm_strict (bool): Whether to use strict LLM filtering (default True).
    """
    logging.info(f"Starting crawl with categories: {categories}, prompt file: '{prompt_file}', max_papers: {max_papers}, total_papers: {total_papers}, start_date: {start_date}, end_date: {end_date}, continue_from_last: {continue_from_last}, llm_strict: {llm_strict}")

    # Prompt user for keywords
    user_input = input("Enter user-defined keywords (separated by spaces): ")
    user_keywords = user_input.split()
    logging.info(f"User-defined keywords: {user_keywords}")
    
    # Read prompt from file
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
        logging.info(f"Prompt read successfully, length: {len(prompt_content)} characters")
    except FileNotFoundError:
        logging.error(f"Prompt file not found: {prompt_file}")
        return
    except IOError as e:
        logging.error(f"Error reading prompt file: {e}")
        return

    # Generate machine-defined keywords with AI using the prompt content
    logging.info("Generating machine-defined keywords with AI...")
    machine_keywords = generate_keywords(prompt_content)
    if not machine_keywords:
        logging.warning("No machine-defined keywords generated. Fetching without keyword refinement.")
    else:
        logging.info(f"Generated machine-defined keywords: {machine_keywords}")

    # Fetch papers from arXiv using categories, user_keywords, and machine_keywords
    logging.info("Fetching papers from arXiv...")
    papers = fetch_arxiv_papers(categories=categories, user_keywords=user_keywords, machine_keywords=machine_keywords, max_results=max_papers, total_results=total_papers, start_date=start_date, end_date=end_date)
    if not papers:
        logging.warning("No papers fetched. Exiting.")
        return
    logging.info(f"Fetched {len(papers)} papers.")

    # If --continue, read filtered_papers.csv and skip already saved papers
    output_file = "filtered_papers.csv"
    existing_titles = set()
    existing_links = set()
    if continue_from_last and os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_titles.add(row.get("Paper Name", "").strip())
                    existing_links.add(row.get("PDF Link", "").strip())
            logging.info(f"Loaded {len(existing_titles)} existing papers from {output_file}.")
        except Exception as e:
            logging.warning(f"Could not read {output_file}: {e}")

    # Filter papers with LLM using the prompt content
    logging.info("Filtering papers with LLM...")
    final_filtered_papers = filter_papers_with_llm(papers, prompt_content, strict=llm_strict)
    logging.info(f"Final filtered down to {len(final_filtered_papers)} papers.")
    if len(final_filtered_papers) == 0:
        logging.warning("No papers passed the LLM filter. Try running with --llm_strict False for less strict filtering.")

    # If --continue, skip papers already in filtered_papers.csv
    if continue_from_last:
        before = len(final_filtered_papers)
        final_filtered_papers = [p for p in final_filtered_papers if p["title"].strip() not in existing_titles and p["pdf_url"].strip() not in existing_links]
        after = len(final_filtered_papers)
        logging.info(f"Skipped {before - after} papers already in {output_file}.")

    # Save to CSV (append if --continue, else overwrite)
    mode = "a" if continue_from_last and os.path.exists(output_file) else "w"
    logging.info(f"Saving to {output_file} (mode: {mode})...")
    try:
        with open(output_file, mode, newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if mode == "w":
                writer.writerow(["Paper Name", "PDF Link"])
            elif mode == "a" and os.path.getsize(output_file) == 0:
                writer.writerow(["Paper Name", "PDF Link"])
            for paper in final_filtered_papers:
                writer.writerow([paper["title"], paper["pdf_url"]])
        logging.info(f"Process complete. Results saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl arXiv for historical papers, filter with keywords and LLM.")
    parser.add_argument("--categories", type=str, required=True, help="Space-separated list of arXiv categories (e.g., 'cs.CV physics.optics')")
    parser.add_argument("--prompt", type=str, required=True, help="Path to the prompt file (e.g., 'my_prompt.txt')")
    parser.add_argument("--max_papers", type=int, required=True, help="Maximum number of papers to retrieve per page (page size)")
    parser.add_argument("--total_papers", type=int, required=True, help="Total number of papers to retrieve")
    parser.add_argument("--start_date", type=str, default='2015-01-01', help="Start date for paper search (YYYY-MM-DD), default: 2015-01-01")
    parser.add_argument("--end_date", type=str, default='', help="End date for paper search (YYYY-MM-DD), default: no end date")
    parser.add_argument("--continue", dest="continue_from_last", action="store_true", help="Continue from last filtered_papers.csv and skip already saved papers.")
    parser.add_argument("--llm_strict", dest="llm_strict", action="store_true", help="Use strict LLM filtering (default: True)")
    parser.add_argument("--no_llm_strict", dest="llm_strict", action="store_false", help="Use less strict LLM filtering (accept any answer starting with 'y')")
    parser.set_defaults(llm_strict=True)

    args = parser.parse_args()
    categories = args.categories.split()
    main(categories=categories, prompt_file=args.prompt, max_papers=args.max_papers, total_papers=args.total_papers, start_date=args.start_date, end_date=args.end_date, continue_from_last=args.continue_from_last, llm_strict=args.llm_strict)