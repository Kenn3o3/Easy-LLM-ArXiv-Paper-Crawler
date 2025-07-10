import os
import logging
from typing import List, Dict, Any
import requests

# Define API key globally here or in Environment Variables
API_KEY = os.getenv("DASHSCOPE_API_KEY")

def call_dashscope_api(prompt: str, max_tokens: int = 50) -> str:
    """Calls the Alibaba Cloud DashScope API (OpenAI-compatible) for text generation."""
    url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-plus",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error calling DashScope API: {e}")
        return ""

def generate_keywords(prompt: str) -> List[str]:
    """Generates a list of keywords using AI based on the provided prompt."""
    api_key = os.getenv("DASHSCOPE_API_KEY", API_KEY)
    if not api_key:
        logging.error("API_KEY is not set. Cannot generate keywords.")
        return []

    # Improved prompt for better keyword reasoning
    ai_prompt = (
        "You are helping to search for relevant research papers on arXiv. "
        "Given the following project description, generate a comma-separated list of search keywords and short phrases that are likely to appear in the title or abstract of relevant arXiv papers. "
        "Include both broad and specific terms, but avoid long or rare phrases. "
        "Favor single words and common two-word phrases. "
        "Do not include explanations or extra text.\n\n"
        f"Project description:\n{prompt}"
    )
    try:
        keywords_str = call_dashscope_api(ai_prompt, max_tokens=100)
        if not keywords_str:
            return []
        # Split by commas and clean up each keyword
        keywords = [kw.strip() for kw in keywords_str.split(",")]
        # Remove duplicates and filter out keywords longer than 3 words
        filtered = []
        seen = set()
        for kw in keywords:
            if kw and kw.lower() not in seen and len(kw.split()) <= 3:
                filtered.append(kw)
                seen.add(kw.lower())
        # Limit to top 10 keywords
        filtered = filtered[:10]
        logging.info(f"Final machine-generated keywords (max 10): {filtered}")
        return filtered
    except Exception as e:
        logging.error(f"Error generating keywords: {e}")
        return []

def filter_papers_with_llm(papers: List[Dict[str, Any]], prompt: str, strict: bool = True) -> List[Dict[str, Any]]:
    """Filters papers using an LLM based on the provided prompt. If strict is False, accept any answer containing 'yes' or starting with 'y'."""
    api_key = os.getenv("DASHSCOPE_API_KEY", API_KEY)
    if not api_key:
        logging.error("API_KEY is not set. Cannot filter papers.")
        return papers

    filtered_papers = []
    for i, paper in enumerate(papers):
        title = paper.get("title", "N/A")
        summary = paper.get("summary", "N/A")

        full_prompt = f"{prompt}\n\nTitle: {title}\nAbstract: {summary}\n\nAnswer with 'yes' or 'no'."
        try:
            answer = call_dashscope_api(full_prompt, max_tokens=5)
            answer_clean = answer.strip().lower()
            logging.info(f"Paper {i+1}/{len(papers)}: '{title[:50]}...'\nPrompt: {full_prompt}\nLLM response: {answer}")
            if strict:
                if answer_clean == "yes" or answer_clean.startswith("yes."):
                    filtered_papers.append(paper)
            else:
                if answer_clean.startswith("y"):
                    filtered_papers.append(paper)
        except Exception as e:
            logging.warning(f"Error filtering paper '{title[:50]}...': {e}")
            continue

    return filtered_papers