---
title: MediAssist Medical Chatbot
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.35.0"
python_version: "3.10"
app_file: app.py
pinned: false
---

# 🏥 MediAssist — Multilingual Medical Support Chatbot

> **GUVI | HCL Final Project** — AI-powered multilingual medical guidance chatbot  
> Built with Python, Streamlit, and OpenAI GPT-4

---

## 📌 Project Overview

**MediAssist** is a multilingual medical support chatbot that:
- Accepts health queries in **any language** (Tamil, Hindi, English, French, Spanish, Arabic, and more)
- **Auto-detects** the input language and translates it to English for processing
- Generates **safe, structured, evidence-based** medical guidance using OpenAI GPT-4
- Translates the response **back to the user's original language**
- Follows strict medical safety rules — never diagnoses, never prescribes

> ⚠️ *This chatbot is not a substitute for professional medical advice.*

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🌐 Multilingual | Supports 10+ languages with auto-detection |
| 🔍 Symptom Analysis | Explains symptoms in simple, clear language |
| ⚠️ Possible Causes | Lists common causes (not diagnosis) |
| 🏥 Home Care Guidance | Practical steps and precautions |
| 🚨 Emergency Detection | Instantly alerts for critical symptoms |
| 💬 Follow-up Questions | Asks clarifying questions for better guidance |
| 🗂️ Chat History | Full conversation context maintained per session |

---

## 🗂️ Project Structure

```
mediassist/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
│
├── utils/
│   ├── __init__.py
│   ├── translator.py         # Language detection & translation (OpenAI)
│   ├── medical_engine.py     # GPT-4 medical response generation
│   ├── session.py            # Streamlit session state management
│   └── helpers.py            # Emergency detection & formatting utilities
│
└── .streamlit/
    └── secrets.toml.example  # Streamlit Cloud deployment config
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API Key ([get one here](https://platform.openai.com/api-keys))
- VS Code (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/mediassist-chatbot.git
cd mediassist-chatbot
```

### Step 2: Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key
```bash
# Copy the template
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 5: Run the App
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Push your code to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo and select `app.py` as the entry point
4. Add `OPENAI_API_KEY` in **Secrets** (Settings → Secrets)
5. Click **Deploy**

### Hugging Face Spaces
1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Streamlit** as the SDK
3. Push your code (including `requirements.txt`)
4. Add `OPENAI_API_KEY` in Space **Settings → Secrets**

---

## 📊 Response Structure

Every MediAssist response follows this safe, structured format:

```
🔍 Symptoms Understanding
   → Clear explanation of what the symptoms mean

⚠️ Possible Causes
   → 3-4 common causes (NOT a diagnosis)

🏥 What You Should Do
   → Practical home care steps & precautions

🚨 When to See a Doctor
   → Red flags that require medical attention

💬 Follow-up Questions
   → Clarifying questions for better guidance

⚠️ Disclaimer (always included)
```

---

## 🛡️ Safety Rules

- ❌ No final diagnosis
- ❌ No prescription drug recommendations
- ❌ No emergency medical decisions
- ✅ Emergency keywords → immediate help alert
- ✅ Medical disclaimer on every response
- ✅ Clear distinction between guidance and medical advice

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | OpenAI GPT-4o |
| Translation | OpenAI GPT-4o-mini |
| Language | Python 3.10+ |
| Deployment | Streamlit Cloud / Hugging Face Spaces |
| Version Control | Git + GitHub |

---

## 📋 Coding Standards

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python coding standards:
- Modular architecture (separate files for each concern)
- Docstrings on all functions and modules
- Meaningful variable and function names
- Proper error handling throughout
- Type hints on function signatures

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**[Your Name]**  
GUVI | HCL AI/ML Program  
[LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

---

> ⚠️ **Medical Disclaimer:** MediAssist provides general health information only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.
