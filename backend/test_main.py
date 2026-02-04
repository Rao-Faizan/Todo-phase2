from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, tasks, chat
import os
from dotenv import load_dotenv
from middleware.rate_limiter import setup_rate_limiter

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# Setup rate limiting
setup_rate_limiter(app)

# CORS configuration
frontend_urls = os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
# Strip whitespace from each URL
frontend_urls = [url.strip() for url in frontend_urls]

# Add OpenAI ChatKit domains
chatkit_domains = [
    "https://chat.openai.com",  # Production ChatKit domain
    "https://chatkit.openai.com",  # Alternative ChatKit domain (placeholder)
]

# Combine all allowed origins
all_origins = frontend_urls + chatkit_domains

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(chat.router, prefix="/api/{user_id}", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}