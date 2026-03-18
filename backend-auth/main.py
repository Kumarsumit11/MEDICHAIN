from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import init_database
from routes import auth, user

# Initialize database
init_database()

# Create FastAPI app
app = FastAPI(
    title="MediSecure Authentication API",
    description="User Authentication and Profile Management",
    version="1.0.0"
)

# CORS middleware
# CORS middleware - SIMPLE FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← Allow ALL origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (only auth and user, no medical)
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {
        "message": "MediSecure Authentication API is running",
        "version": "1.0.0",
        "endpoints": {
            "auth": {
                "register": "POST /api/auth/register",
                "login": "POST /api/auth/login"
            },
            "user": {
                "get_profile": "GET /api/user/{phone}",
                "get_qr_data": "GET /api/user/qr/{phone}",
                "update_profile": "PUT /api/user/{phone}"
            }
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "authentication"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)