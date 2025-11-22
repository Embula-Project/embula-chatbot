# Embula Restaurant Chatbot Backend (Python FastAPI)

This is the **Python FastAPI** version of the **Embula Restaurant Chatbot backend**, powered by **Mistral AI**. It handles:

- Menu queries (filter by vegan/vegetarian/non-veg)  
- Table availability & reservations  
- Restaurant info (location, contact, opening hours)  
- Safe SQL access (restricted tables are blocked)  
- Frontend integration ready

---

## Features

- **FastAPI**: High-performance, easy-to-learn, production-ready framework  
- **Mistral AI Integration**: Uses `mistral-small-latest` for intelligent natural language understanding  
- **Context Awareness**: Maintains conversation history per session (in-memory)  
- **System Personality**: Friendly restaurant assistant  
- **Profanity & SQL Injection Filter**: Sanitizes user input using `better-profanity` and a custom sanitizer  
- **Database-Safe Queries**: Only reads from allowed tables: `food_item`, `food_item_ingredients`, `reservations`, `restaurant_tables`, `discounts`  
- **Frontend Integration Ready**: API endpoints can be called via JS, React, Next.js, or any frontend

---

## Project Structure


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

 1.**Prerequisites**

- Python 3.9+  
- MySQL 8+ (if using a real database)  
- Mistral AI API Key  
- `pip` package manager  
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
