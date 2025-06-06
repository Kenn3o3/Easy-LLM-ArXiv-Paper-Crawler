# Project: ArXiv Historical Paper Crawler with LLM Filtering

This project enables users to crawl arXiv for papers from specified categories, filter them using a Large Language Model (LLM) based on a custom prompt, and generate a CSV file with the filtered paper names and PDF links. Unlike daily crawlers, this project fetches historical papers up to a user-defined maximum, making it ideal for comprehensive research collection.

## Features

- **User Inputs**:
  - List of arXiv categories (e.g., `cs.CV`, `physics.optics`).
  - Custom LLM prompt for filtering papers (e.g., "Is this paper about image generation?").
  - Maximum number of papers to retrieve.

- **Functionality**:
  - Crawls arXiv for papers in the specified categories, including historical papers.
  - Uses an LLM (via Alibaba Cloud DashScope API) to filter papers based on the provided prompt.
  - Outputs a CSV file (`filtered_papers.csv`) with columns: `Paper Name`, `PDF Link`.

- **Automation**:
  - Fetches papers in batches, starting from the most recent, until the maximum number is reached or no more papers are available.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Kenn3o3/Easy-LLM-ArXiv-Paper-Crawler.git
   cd arxiv_crawler
   ```

2. **Create and Activate a Virtual Environment** (Recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Key**:
   This project uses Alibaba Cloud's DashScope API for LLM filtering. Follow these steps to set up your API key:
   - **Obtain an API Key**:
     - Go to the [Alibaba Cloud console](https://www.alibabacloud.com/help/en/model-studio) and navigate to the DashScope section.
     - Create a new API key if you don't have one.
   - **Set the Environment Variable**:
     - On Windows PowerShell: `$env:DASHSCOPE_API_KEY = "your_api_key_here"`
     - On macOS/Linux: `export DASHSCOPE_API_KEY="your_api_key_here"`
     - Replace `"your_api_key_here"` with your actual API key.
   - You can also set this in your shell configuration file (e.g., `~/.bashrc`) for persistent access.
   - **Important**: Do not commit your API key to version control.

## Usage

Run the main script with the required arguments:

```bash
python main.py --categories "cs.CV physics.optics" --prompt my_prompt.txt --max_papers 100
```

- `--categories`: Space-separated list of arXiv categories (quoted if multiple).
- `--prompt`: Path to a text file containing the LLM prompt to filter papers.
- `--max_papers`: Maximum number of papers to retrieve.

The script will:
1. Crawl arXiv for historical papers in the specified categories.
2. Filter them using the LLM based on the prompt.
3. Save the results to `filtered_papers.csv`.

### How to Write the Prompt

The prompt is used to filter papers using the LLM. It should be a clear question or statement that the LLM can answer based on the paper's abstract or title. For example:
- "Is this paper about image generation?"
- "Does this paper discuss quantum computing algorithms?"

Ensure the prompt is specific enough to filter out irrelevant papers but broad enough to capture all relevant ones. Save the prompt in a text file (e.g., `my_prompt.txt`).

### Example Output

The `filtered_papers.csv` file will contain rows like this:

```
Paper Name,PDF Link
"Deep Learning for Image Recognition","https://arxiv.org/pdf/1234.5678.pdf"
"Advances in Quantum Computing Algorithms","https://arxiv.org/pdf/9012.3456.pdf"
```

This format helps users understand the output structure.

## Project Structure

```
.
├── main.py             # Main execution script
├── arxiv_crawler.py    # Module for crawling arXiv papers
├── llm_filter.py       # Module for filtering papers using LLM
├── utils.py            # Utility functions (e.g., CSV writing)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Dependencies

- `arxiv`: For interacting with the arXiv API.
- `requests`: For making Alibaba Cloud DashScope API calls.

Note: The `csv` module is part of Python's standard library and does not require installation.

## Notes

- **Historical Crawling**: Papers are fetched starting from the most recent, moving backward in time, until the maximum number is reached or no more papers are available.
- **API Rate Limits**: The script includes delays to respect arXiv and DashScope API rate limits. Fetching a large number of papers may take time due to these limits.
- **LLM Costs**: Filtering many papers may incur costs from the DashScope API; test with a small `max_papers` value first.

### Common Categories for Embodied AI

Embodied AI refers to artificial intelligence systems integrated with physical bodies or robots, enabling interaction with the physical world. Common arXiv categories related to Embodied AI include:
- `cs.AI`: Artificial Intelligence
- `cs.CV`: Computer Vision
- `cs.RO`: Robotics
- `cs.HC`: Human-Computer Interaction

Example command for Embodied AI research: (I recommend running on a single category for more precise result)
```bash
python main.py --categories "cs.RO" --prompt my_prompt.txt --max_papers 100
```