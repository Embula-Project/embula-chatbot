from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import chat
from src.config import settings

app = FastAPI(title="Embula Chatbot API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Embula Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
