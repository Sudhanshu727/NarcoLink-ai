# NarcoLinkAI : Social Media Drug Dealer Detection

**Authors:**
*   Soumya Sourav Das ([@celestial317](https://github.com/celestial317))
*   Sudhanshu Shekhar ([@s17](https://github.com/s17))
*   Devyanshi Bansal ([@DevyanshiBansal](https://github.com/DevyanshiBansal))

> **Built for Shield 1.0 Hackathon**  
> Organized by **CDTI Jaipur** under **BPRD, Govt of India**

---

## About The Project

**NarcoLinkAI** is an advanced intelligence system designed to detect and analyze drug trafficking activities on social media and the dark web. Traditional keyword-based detection fails against evolving drug slang and multimodal content (text + images). NarcoLinkAI bridges this gap using **Vector Alchemy** for slang deciphering, **Multimodal LLMs** for context-aware risk assessment, and an **Autonomous Agent (Zoro)** for dark web OSINT.

## Unique Selling Points (USP) & Novelty

*   **Vector Alchemy & Slang Decoding:** Unlike static dictionaries, our "Vector Alchemy" approach treats words as vectors. By subtracting "innocent" semantic properties and adding "drug" properties, the system can dynamically uncover hidden meanings in new slang (e.g., detecting "snow" as Cocaine based on context).
*   **Multimodal Detection (Text + Image):** We utilize **Gemma** and **Image Embeddings** to analyze posts containing both text and images. This allows the system to understand context that text-alone models miss (e.g., a photo of white powder with the caption "Fresh snow").
*   **Zoro (Agentic Dark Web OSINT):** An autonomous AI agent that navigates the dark web using Tor. It iteratively refines its search queries, filters results using an LLM, and recursively crawls .onion sites to generate actionable intelligence reports.
*   **Privacy-First & Local First:** The core analysis runs efficiently with local components, minimizing external data leakage.

## Tech Stack

*   **Backend:** FastAPI (Python), Uvicorn
*   **AI/ML:** PyTorch, LangChain, Gemma (via OpenRouter/Local), OpenAI/OpenRouter API
*   **Vector Database/Embeddings:** Torch (Vector operations), Custom Bloom Filter Engine
*   **Dark Web:** Tor (SOCKS5 Proxy), Requests, BeautifulSoup
*   **Frontend:** React, Vite, TailwindCSS

## Setup & Installation

### Prerequisites
1.  **Python 3.9+**
2.  **Node.js & npm**
3.  **Tor Browser** (Must be running for Dark Web extraction to work)
4.  **OpenRouter API Key** (for LLM capabilities)

### Backend Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/celestial317/drugDealerDetection_BPRD_Shield.git
    cd drugDealerDetection_BPRD_Shield
    ```

2.  Install Python dependencies:
    ```bash
    pip install fastapi uvicorn torch transformers nltk yaspin beautifulsoup4 requests python-dotenv langchain_openai langchain_core
    ```
    *(Note: Ensure you have PyTorch installed appropriately for your system hardware)*

3.  Configure Environment:
    Create a `.env` file in the root directory and add your key:
    ```
    OPENROUTER_API_KEY=your_api_key_here
    ```

4.  Start the Backend:
    ```bash
    python main.py
    ```
    The API will run at `http://0.0.0.0:8000`.

### Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Start the Development Server:
    ```bash
    npm run dev
    ```
    The application will launch at `http://localhost:5173`.

## How It Works

### 1. Social Media Analysis
*   **Input:** Users upload a screenshot, image, or text caption.
*   **Processing:**
    *   **Image:** Processed via `ImageEmbedder` and `GemmaIntake` to extract visual context.
    *   **Text:** `DrugDecoder` analyzes text using Vector Alchemy to detect hidden slang.
    *   **Fusion:** Data is fused in the `DrugDetectionEngine` to assign a Risk Level (High/Low).
*   **Output:** A detailed breakdown of detected entities, slang meanings, and overall risk.

### 2. Zoro (Dark Web Extractor)
*   **Input:** A target query (e.g., specific drug name or vendor alias).
*   **Agentic Loop:**
    1.  **Refine:** The Agent refines the query into effective dark web search terms.
    2.  **Search:** Queries multiple Tor search engines (Ahmia, OnionLand, etc.).
    3.  **Filter:** Uses LLM to select the most relevant results.
    4.  **Crawl:** Recursively visits .onion links to depth `N` to scrape content.
*   **Output:** Generates a comprehensive Intelligence Report in Markdown.

Built for a safer society.
