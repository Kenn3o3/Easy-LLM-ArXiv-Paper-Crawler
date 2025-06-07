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
       export DASHSCOPE_API_KEY="your_api_key_here"
       ```  
     - Windows PowerShell:  
       ```bash
       $env:DASHSCOPE_API_KEY = "your_api_key_here"
       ```  
   - Replace `"your_api_key_here"` with your actual key.  
   - **⚠️ Don’t share your API key!**

---

## 🚀 How to Use It

Run this command in your terminal:  
```bash
python main.py --categories "cs.CV" --prompt my_prompt.txt --max_papers 10
```

### What the Options Mean:
- `--categories`: The arXiv category you want (e.g., `cs.CV` for computer vision).  
- `--prompt`: A text file with a question to filter papers (e.g., `my_prompt.txt`).  
- `--max_papers`: How many papers to get (e.g., `100`).  

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

---

## 📝 Extra Tips
- It grabs older papers, not just new ones.  
- Don’t ask for too many papers at once—there are API limits.  
- Use specific categories and a clear prompt for better results.  
- Common categories: `cs.AI` (AI), `cs.CV` (vision), `cs.RO` (robotics).  

Enjoy finding papers that match your interests!

## 📊 Repository Views

[![Visitors](https://api.visitorbadge.io/api/combined?path=https%3A%2F%2Fgithub.com%2FKenn3o3%2FEasy-LLM-ArXiv-Paper-Crawler&countColor=%23dce775)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FKenn3o3%2FEasy-LLM-ArXiv-Paper-Crawler)

