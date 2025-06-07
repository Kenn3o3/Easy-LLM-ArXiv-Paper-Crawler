import argparse
import logging
import os
from arxiv_crawler import fetch_arxiv_papers
from llm_filter import generate_keywords, filter_papers_with_llm
from utils import save_to_csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(categories, prompt_file, max_papers):
    """
    Main function to crawl arXiv, filter papers using keywords and LLM, and save to CSV.
    
    Args:
        categories (list): List of arXiv categories.
        prompt_file (str): Path to the file containing the LLM prompt.
        max_papers (int): Maximum number of papers to retrieve.
    """
    logging.info(f"Starting crawl with categories: {categories}, prompt file: '{prompt_file}', max_papers: {max_papers}")

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
    papers = fetch_arxiv_papers(categories=categories, user_keywords=user_keywords, machine_keywords=machine_keywords, max_results=max_papers)
    if not papers:
        logging.warning("No papers fetched. Exiting.")
        return
    logging.info(f"Fetched {len(papers)} papers.")

    # Filter papers with LLM using the prompt content
    logging.info("Filtering papers with LLM...")
    final_filtered_papers = filter_papers_with_llm(papers, prompt_content)
    logging.info(f"Final filtered down to {len(final_filtered_papers)} papers.")

    # Save to CSV
    output_file = "filtered_papers.csv"
    logging.info(f"Saving to {output_file}...")
    save_to_csv(final_filtered_papers, output_file)
    logging.info(f"Process complete. Results saved to {output_file}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl arXiv for historical papers, filter with keywords and LLM.")
    parser.add_argument("--categories", type=str, required=True, help="Space-separated list of arXiv categories (e.g., 'cs.CV physics.optics')")
    parser.add_argument("--prompt", type=str, required=True, help="Path to the prompt file (e.g., 'my_prompt.txt')")
    parser.add_argument("--max_papers", type=int, required=True, help="Maximum number of papers to retrieve")

    args = parser.parse_args()
    categories = args.categories.split()
    main(categories=categories, prompt_file=args.prompt, max_papers=args.max_papers)