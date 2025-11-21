# Embula Restaurant Chatbot Backend (Python FastAPI)

This is the Python FastAPI version of the Embula Restaurant Chatbot backend, powered by Mistral AI.

## Features
- **FastAPI**: High-performance, easy-to-learn, fast-to-code, ready-for-production web framework.
- **Mistral AI Integration**: Uses `mistral-small-latest` for intelligent responses.
- **Context Aware**: Maintains conversation history per session (in-memory).
- **System Personality**: Configured to be a friendly restaurant assistant.
- **Profanity Filter**: Blocks inappropriate language using `better-profanity`.

## Project Structure
```
embula-chatbot-python/
├── src/
│   ├── config/         # Configuration settings
│   ├── models/         # Pydantic models
│   ├── routers/        # API endpoints
│   ├── services/       # Business logic
│   ├── utils/          # Helpers (Memory store)
│   └── main.py         # Application entry point
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## Setup Instructions

1.  **Prerequisites**: Python 3.9+ installed.
2.  **Create Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment**:
    - Open `.env` file.
    - Add your Mistral API Key: `MISTRAL_API_KEY=your_actual_key_here`

5.  **Run the Server**:
    ```bash
    # Run from the root directory
    python src/main.py
    # OR using uvicorn directly
    uvicorn src.main:app --reload
    ```

## API Endpoints

### 1. Chat with Bot
**POST** `/api/chat`

**Body:**
```json
{
  "message": "What is on the menu?",
  "sessionId": "user-123"
}
```

**Response:**
```json
{
  "reply": "We offer a variety of dishes including...",
  "usage": { ... }
}
```

### 2. Clear History
**DELETE** `/api/chat/history/{session_id}`

## Deployment (Render / Railway / Vercel)

1.  **Push to GitHub**.
2.  **Link to Provider**.
3.  **Environment Variables**: Add `MISTRAL_API_KEY`.
4.  **Build Command**: `pip install -r requirements.txt`.
5.  **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`.
