# 🏛️ CivicBridge

> **Bridging citizens with the information they need to understand and access government services.**

CivicBridge is an AI-powered civic assistance platform designed to help citizens understand government schemes, services, and documents through a simple conversational interface.

The platform combines a modern web interface, a FastAPI backend, document processing, a knowledge base, and Google's Gemini AI to provide accessible and contextual responses to civic-related queries.

---

## ✨ Features

* 🤖 **AI-Powered Civic Assistant**

  * Ask questions about government schemes, services, and civic processes.
  * Receive natural-language responses through a conversational interface.

* 📄 **Document Analysis**

  * Upload supported PDF documents.
  * Extract and analyze information from uploaded documents.
  * Use document content as context for AI-powered responses.

* 📚 **Knowledge Base**

  * Provides the AI system with relevant civic and government information.
  * Helps generate responses grounded in the project's available knowledge.

* 💬 **Interactive Chat Interface**

  * Simple and user-friendly interface for interacting with CivicBridge.

* 🔐 **Environment-Based Configuration**

  * API keys and deployment-specific configuration are managed using environment variables.

* 🌐 **Deployment Ready**

  * Frontend can be deployed separately from the FastAPI backend.
  * CORS configuration supports both local development and deployed frontend environments.

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │      User           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   CivicBridge       │
                    │   Frontend          │
                    │   Next.js           │
                    └──────────┬──────────┘
                               │
                         HTTP / API
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌──────────────┐   ┌────────────┐
       │ Chat API   │   │ Document API │   │ Knowledge  │
       │            │   │              │   │ Base       │
       └─────┬──────┘   └──────┬───────┘   └─────┬──────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │    Gemini AI        │
                    │    Integration      │
                    └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

* **Next.js**
* **React**
* **TypeScript**
* CSS / frontend styling

### Backend

* **Python**
* **FastAPI**
* **Uvicorn**
* **Pydantic**
* **CORS Middleware**

### AI

* **Google Gemini API**
* AI-powered conversational responses
* Document/context-based analysis

### Development & Deployment

* **Git / GitHub**
* Frontend deployment: **Vercel**
* Backend deployment: **Render**

---

## 📁 Project Structure

```text
Code_Blooded/
│
├── backend/
│   ├── ai/
│   │   └── gemini.py
│   │
│   ├── api/
│   │   ├── chat.py
│   │   └── document.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx
│   │       └── ...
│   │
│   ├── package.json
│   └── ...
│
├── README.md
└── ...
```

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/nndev3447/Code_Blooded.git
cd Code_Blooded
```

---

# 🔧 Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

### Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file inside the backend directory.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
```

> **Important:** Never commit API keys or other secrets to GitHub.

### Start the backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation can be accessed at:

```text
http://localhost:8000/docs
```

---

# 💻 Frontend Setup

Open a new terminal and navigate to the frontend:

```bash
cd frontend
```

### Install dependencies

```bash
npm install
```

### Configure the backend URL

Create a `.env.local` file if required by the frontend configuration.

Example:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, replace the local backend URL with the deployed backend URL.

### Start the development server

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:3000
```

---

# 🔑 Environment Variables

The project uses environment variables to keep configuration and secrets outside the source code.

### Backend

| Variable         | Description                                    |
| ---------------- | ---------------------------------------------- |
| `GEMINI_API_KEY` | API key used to communicate with Google Gemini |

### Frontend

| Variable              | Description                        |
| --------------------- | ---------------------------------- |
| `NEXT_PUBLIC_API_URL` | URL of the CivicBridge backend API |

> Do not commit `.env`, `.env.local`, API keys, or other secrets to the repository.

---

# 🔌 API Overview

The FastAPI backend provides endpoints for interacting with CivicBridge.

### Health Check

```http
GET /
```

Used to verify that the backend is running.

### Chat

The chat API handles user questions and generates AI-powered responses.

### Document Processing

The document API handles supported document uploads and processing.

Only supported PDF documents are accepted by the document upload functionality.

For complete endpoint details, run the backend and visit:

```text
http://localhost:8000/docs
```

---

# 📄 Document Processing

CivicBridge supports PDF-based document analysis.

The general workflow is:

```text
PDF Upload
    ↓
Document Validation
    ↓
Text Extraction
    ↓
Relevant Information Processing
    ↓
Context Provided to AI
    ↓
AI-Generated Response
```

Non-PDF files are rejected by the backend with an appropriate error response.

---

# 🤖 AI Workflow

CivicBridge uses Gemini to provide natural-language responses.

A simplified workflow is:

```text
User Question
      ↓
Frontend
      ↓
FastAPI Backend
      ↓
Relevant Context / Knowledge Base
      ↓
Gemini API
      ↓
Generated Response
      ↓
Frontend
      ↓
User
```

For document-related queries, uploaded document content can be incorporated into the processing flow to provide context for the response.

---

# 🌐 Deployment

CivicBridge can be deployed as two separate services:

```text
                    Internet
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       ┌───────────┐       ┌───────────┐
       │  Vercel   │       │  Render   │
       │ Frontend  │──────▶│  Backend  │
       └───────────┘       └───────────┘
```

### Frontend

The Next.js frontend can be deployed using **Vercel**.

### Backend

The FastAPI backend can be deployed using **Render**.

The deployed frontend must be configured to communicate with the deployed backend URL.

CORS settings in the backend should allow requests from the deployed frontend.

---

# 🔒 Security

* API keys are stored using environment variables.
* Secrets should never be committed to Git.
* CORS should be configured to allow only trusted frontend origins in production.
* Uploaded documents should be validated before processing.

---

# 🧪 Testing

The application can be tested at multiple levels:

### Frontend

* Verify that the interface loads correctly.
* Test sending chat messages.
* Test PDF uploads.
* Verify API responses are displayed correctly.

### Backend

* Verify the FastAPI server starts successfully.
* Test API endpoints through `/docs`.
* Test valid PDF uploads.
* Test invalid file uploads.
* Verify appropriate error responses.

### Deployment

* Verify the frontend can communicate with the deployed backend.
* Check browser console/network errors.
* Verify CORS configuration.
* Confirm environment variables are correctly configured.

---

# 📌 Future Improvements

Potential future improvements include:

* Support for additional document formats.
* Improved document retrieval and contextual search.
* More comprehensive government-service knowledge.
* Multilingual civic assistance.
* Voice-based interaction.
* Personalized service recommendations.
* Improved citation and source transparency.
* Additional authentication and user-specific features.

---

# 🎯 Project Goal

CivicBridge aims to make civic information easier to understand and access by combining conversational AI with structured civic knowledge and document analysis.

The goal is to reduce the complexity of navigating government-related information and provide citizens with a more accessible way to find relevant information.

---

## 👥 Team

**Code Blooded**

Built as part of a hackathon project.

---

## 📜 License

This project is intended for educational and hackathon purposes.

Add an appropriate open-source license here if the project is released under one.
