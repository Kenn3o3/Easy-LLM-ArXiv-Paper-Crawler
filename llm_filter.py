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

    # Updated prompt for a clean, comma-separated list
    ai_prompt = f"Generate a comma-separated list of keywords relevant to the following topic: {prompt}. Do not include any explanations or additional text."
    try:
        keywords_str = call_dashscope_api(ai_prompt, max_tokens=50)
        if not keywords_str:
            return []
        # Split by commas and clean up each keyword
        keywords = [kw.strip() for kw in keywords_str.split(",")]
        return keywords
    except Exception as e:
        logging.error(f"Error generating keywords: {e}")
        return []

def filter_papers_with_llm(papers: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
    """Filters papers using an LLM based on the provided prompt."""
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
            answer = answer.strip().lower()
            logging.info(f"Paper {i+1}/{len(papers)}: '{title[:50]}...' - LLM response: {answer}")
            if "yes" in answer:
                filtered_papers.append(paper)
        except Exception as e:
            logging.warning(f"Error filtering paper '{title[:50]}...': {e}")
            continue

    return filtered_papers