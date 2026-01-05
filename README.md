# 💰 Smart Finance Advisor

**A Generative AI-powered application that turns static receipts into actionable financial data.**

### 🚀 Introduction
Managing daily expenses and organizing physical receipts is often tedious. **Smart Finance Advisor** solves this by acting as an intelligent assistant. Instead of manually typing data into spreadsheets, users can simply upload a picture of a bill (or snap one with their webcam) and chat with it.

Whether you want to know the tax amount, check if you bought specific items, or automatically log the expense to a database, just ask.

### ✨ Key Features
* **Chat with your Bill:** Uses Large Language Models (LLMs) to understand receipt context and answer natural language queries.
* **Hybrid Input:** Seamlessly switch between **File Upload** and **Live Camera** based on your convenience.
* **Privacy-First Design:** Camera toggle ensures the webcam is active only when you need it.
* **Auto-Log Intelligence:** Detects commands like *"Save this bill"* and automatically extracts structured data (Merchant, Date, Total) into JSON format for storage.

### 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based UI)
* **AI Logic:** [LangChain](https://www.langchain.com/) (Orchestration)
* **Model:** GPT-4o-mini / Gemini Flash (via OpenRouter)
* **Image Processing:** Pillow (PIL)
* **Language:** Python 3.10+

### ⚙️ How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/vanshkhare16106/FINANCE-ADVISOR-MACS.git](https://github.com/vanshkhare16106/FINANCE-ADVISOR-MACS.git)
    cd finance-advisor
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API Key**
    * Create a file named `.env` in the root folder.
    * Add your OpenRouter (or OpenAI) API key:
        ```env
        OPENROUTER_API_KEY=sk-or-v1-your-key-here
        ```

4.  **Run the application**
    ```bash
    streamlit run app.py
    ```

### 📂 Project Structure
```text
📦 finance-advisor
 ┣ 📜 app.py             # Main frontend interface (Streamlit)
 ┣ 📜 chain.py           # Backend AI logic & prompt engineering
 ┣ 📜 requirements.txt   # List of dependencies
 ┣ 📜 .env               # API Secrets (Not uploaded to GitHub)
 ┗ 📜 README.md          # Project Documentation
