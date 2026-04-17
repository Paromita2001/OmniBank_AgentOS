# 🏦 OmniBank Agent OS  
### AI-Powered Banking Assistant with Analytics Dashboard

---

## 🚀 Overview

OmniBank Agent OS is an AI-powered banking assistant built using a multi-agent architecture.  
It combines conversational AI, financial analytics, and automation into a single intelligent system.

Users can interact through chat to:
- Check balance
- Transfer money
- View transaction history
- Analyze spending patterns
- Get AI-driven financial insights

---

## 🎯 Key Features

### 💬 Conversational Banking
- Natural language chat interface
- Handles balance checks, transfers, and history queries

### 📊 Smart Analytics Dashboard
- Category-wise spending breakdown (donut + bar charts)
- Monthly trend visualization
- Comparison (this month vs last month)
- Percentage increase/decrease tracking

### 🔮 AI Insights & Predictions
- Personalized saving suggestions
- Future spending prediction

### ⏰ Reminder System
- Add and manage reminders using natural language

### 📚 RAG-based Knowledge System
- Retrieves banking-related FAQs
- Falls back to LLM when needed

---

## 🧠 Architecture

The system follows a **multi-agent architecture using LangGraph**:


User Input
↓
Intent Parser (LLM)
↓
Routing (Graph)
↓
Agents:

Bank Agent
Analytics Agent
Reminder Agent
RAG Agent
Fallback Agent
↓
Response + UI Visualization

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** Groq (LLaMA 3)
- **Framework:** LangGraph
- **Database:** SQLite
- **Visualization:** Plotly
- **Embeddings / RAG:** FAISS

---

## 📂 Project Structure


OmniBank_AgentOS/
│
├── agents/ # All AI agents (bank, analytics, reminder, etc.)
├── db/ # Database operations
├── pipeline/ # Intent parsing + LLM logic
├── graph/ # LangGraph flow
├── interface/ # Streamlit UI
├── services/ # Supporting services (auth, notifications)
├── data/ # RAG documents
├── vectorstore/ # FAISS index
├── app.py # Entry point
└── requirements.txt


💡 Challenges Solved
Handling inconsistent LLM outputs (intent + entities)
Syncing UI with backend analytics
Managing multi-agent orchestration
Debugging real-world merge conflicts and system flow


🚀 Future Improvements
Voice-based interaction
Real-time bank API integration
Advanced fraud detection
Personalized financial planning


👩‍💻 Author

Paromita Karmakar
MSc Data Science

⭐ If you like this project

Give it a ⭐ on GitHub and share feedback!
