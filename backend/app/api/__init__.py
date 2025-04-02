from fastapi import APIRouter
from app.api import auth, pets, adoptions, visits

# Create main API router
api_router = APIRouter()

# Include auth routes with proper prefix
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include pet routes with proper prefix
api_router.include_router(pets.router, prefix="/pets", tags=["pets"])

# Include adoption application routes with proper prefix
api_router.include_router(adoptions.router, prefix="/adoptions", tags=["adoptions"])

# Include visit scheduling routes with proper prefix
api_router.include_router(visits.router, prefix="/visits", tags=["visits"])