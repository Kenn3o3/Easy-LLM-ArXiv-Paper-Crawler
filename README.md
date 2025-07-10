# 🌟 ArXiv Historical Paper Crawler with LLM Filtering 📚

This tool helps you find research papers from [arXiv](https://arxiv.org/) that match your interests. It searches historical papers in specific categories, filters them using a custom question, and saves the results to a file.

---

## 🛠️ Installation

Follow these steps to set it up:

1. **Clone the repository**  
   Open your terminal and run:  
   ```bash
   git clone https://github.com/Kenn3o3/Easy-LLM-ArXiv-Paper-Crawler.git
   ```

2. **Go to the folder**  
   ```bash
   cd Easy-LLM-ArXiv-Paper-Crawler
   ```

3. **Create a virtual environment**  
   ```bash
   python3 -m venv .venv
   ```

4. **Activate the virtual environment**  
   - On macOS/Linux:  
     ```bash
     source .venv/bin/activate
     ```  
   - On Windows:  
     ```bash
     .venv\Scripts\activate
     ```

5. **Install required packages**  
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up the API key** 🔑  
   - Get an API key from [Alibaba Cloud DashScope](https://bailian.console.alibabacloud.com).  
   - Add it to your system:  
     - macOS/Linux:  
       ```bash
       export DASHSCOPE_API_KEY="sk-***"
       ```  
     - Windows PowerShell:  
       ```bash
       $env:DASHSCOPE_API_KEY = "sk-***"
       ```  
   - Replace `"your_api_key_here"` with your actual key.  
   - **⚠️ Don’t share your API key!**

---

## 🚀 How to Use It

Run this command in your terminal:  
```bash
python main.py --categories "cs.CV" --prompt my_prompt.txt --max_papers 10 --total_papers 50 --start_date 2015-01-01
```

Or, to **continue from your last run** and avoid saving duplicate papers:
```bash
python main.py --categories "cs.CV" --prompt my_prompt.txt --max_papers 10 --total_papers 50 --start_date 2015-01-01 --continue
```

### What the Options Mean:
- `--categories`: The arXiv category you want (e.g., `cs.CV` for computer vision).  
- `--prompt`: A text file with a question to filter papers (e.g., `my_prompt.txt`).  
- `--max_papers`: How many papers to get per page (e.g., `100`).  
- `--total_papers`: Total number of papers to fetch (e.g., `200`).
- `--start_date`: (Optional) Start date for paper search in `YYYY-MM-DD` format. **Default: 2015-01-01** (fetches papers from 2015 onward).
- `--end_date`: (Optional) End date for paper search in `YYYY-MM-DD` format. Leave blank to include up to the most recent papers.
- `--continue`: (Optional) If set, the script will continue from the last `filtered_papers.csv` and only append new, non-duplicate papers. This prevents saving the same paper twice if you run the script multiple times.

After running, type some keywords in the terminal. Only papers with these keywords in the title or abstract will be kept.

### ✍️ Making the Prompt File
Create a file (e.g., `my_prompt.txt`) with a simple question like:  
- "Is this paper about image generation?"  
- "Does this paper talk about robotics?"  

The tool uses this to decide which papers to keep.

### 📄 What You Get
The results are saved in `filtered_papers.csv` with:  
- `Paper Name`  
- `PDF Link`  

If you use `--continue`, new results will be appended to the CSV, and any duplicates (by title or PDF link) will be skipped automatically.

---

## 📝 Extra Tips
- It now grabs older papers by default (from 2015 onward), not just new ones.  
- Don’t ask for too many papers at once—there are API limits.  
- Use specific categories and a clear prompt for better results.  
- Common categories: `cs.AI` (AI), `cs.CV` (vision), `cs.RO` (robotics).  

Enjoy finding papers that match your interests!

## 📊 Repository Views

[![Visitors](https://api.visitorbadge.io/api/combined?path=https%3A%2F%2Fgithub.com%2FKenn3o3%2FEasy-LLM-ArXiv-Paper-Crawler&countColor=%23dce775)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FKenn3o3%2FEasy-LLM-ArXiv-Paper-Crawler)

## New Features and Improvements

- **Machine-generated keywords are now limited to 10 for more focused queries.
- If too few papers are fetched, the crawler will retry with only user keywords (no machine keywords).
- LLM filtering now supports a strict mode (default) and a less strict mode (accepts any answer starting with 'y').
- Use `--llm_strict` (default) for strict filtering, or `--no_llm_strict` for less strict filtering.
- Improved logging for debugging queries and LLM responses.

## Usage

```bash
python main.py --categories "cs.CV" --prompt my_prompt.txt --max_papers 100 --total_papers 500 --start_date 2020-01-01 --llm_strict
```

- To use less strict LLM filtering (recommended if you get 0 results):

```bash
python main.py --categories "cs.CV" --prompt my_prompt.txt --max_papers 100 --total_papers 500 --start_date 2020-01-01 --no_llm_strict
```

## Troubleshooting

- **No papers fetched:**
  - Try reducing the number of keywords or using only user keywords.
  - Check your internet connection and arXiv API status.
- **No papers pass the LLM filter:**
  - Try running with `--no_llm_strict` for less strict filtering.
  - Review the prompt in `my_prompt.txt` to ensure it is not too restrictive.
- **Still empty results?**
  - Try a broader category or simpler keywords.
  - Check the logs for query and LLM response details.

