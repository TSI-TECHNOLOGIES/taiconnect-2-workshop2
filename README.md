# AI-Powered Healthcare – Smarter Patient Management & Diagnosis

## 📋 Overview
This project showcases an AI-powered healthcare system designed to streamline patient management and diagnosis. It leverages AI models to analyze patient data and facilitate appointment bookings.

## 📁 Project Structure
```
├── .dockerignore
├── .gitignore
├── BackEnd
│   ├── .env
│   ├── .env.example
│   ├── Dockerfile
│   ├── KB_PDF
│   │   └── Hospital Overview - Doctors.pdf
│   ├── config.json
│   ├── data
│   │   ├── doctorData.csv
│   │   └── patientData.csv
│   ├── main.py
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── controller
│       │   └── patient_controller.py
│       ├── functions
│       │   └── custom_functions.py
│       ├── models
│       │   └── models.py
│       ├── tools
│       │   ├── tool_constructor.py
│       │   └── tool_execution.py
│       ├── utils
│       │   ├── chunk_embedder.py
│       │   ├── llm_call.py
│       │   └── prompt_constructor.py
│       └── vectorDB
│           ├── 4bdbea04-0eeb-4288-917d-2df3b3e4027d
│           └── chroma.sqlite3
├── FrontEnd
│   ├── .streamlit
│   │   └── config.toml
│   ├── Dockerfile
│   ├── assert
│   │   └── user_profile.png
│   ├── audio
│   │   ├── __init__.py
│   │   ├── input
│   │   └── output
│   ├── audio_handler.py
│   ├── config.json
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yaml
```

## 🐳 Docker Setup
### ✅ Clone the repository
```bash
git clone https://github.com/TSI-TECHNOLOGIES/taiconnect-2-workshop2.git
cd taiconnect-2-workshop2
```

## ⚙️ Prerequisites
1. Set up environment variables:
    - Copy `.env.example` to `.env` inside the `BackEnd/` folder.
    - Fill in the following fields in the `.env` file:
      ```env
      groq_api_key="your_groq_api_key"
      openai_api_key="your_openai_api_key"
      sender_email_ID="your_gmail_id"
      sender_email_password="your_gmail_password"
      ```
2. Follow the instructions provided in the **Prerequisites PDF**(Which is sent via mail) to create necessary accounts and obtain API keys.

### ✅ Build and Run the Containers
For **Windows**, **Mac**, and **Linux**, run:
```bash
docker-compose up --build
```

This command builds the Docker images and starts both the **frontend** and **backend** containers.

## 🌐 Accessing the Application
- **Frontend (Streamlit):** [http://localhost:8501](http://localhost:8501)
- **Backend (FastAPI Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

## 🛠️ Troubleshooting
- Ensure Docker is installed and running on your system.
- If ports `8501` or `8000` are occupied, modify the `docker-compose.yaml` to use different ports.
- Verify API keys and credentials in `.env` if you encounter authentication errors.

## 📖 Additional Notes
- Update `.env` with accurate API keys and credentials before running the app.
- The backend includes a **vectorDB** folder for managing embeddings and data storage.

---
Happy Coding! 🚀
