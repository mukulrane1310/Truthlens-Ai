"""Central API router - registers all module routers."""
from fastapi import APIRouter

from app.modules.auth.api import router as auth_router
from app.modules.claims.api import router as claims_router
from app.modules.evidence.api import router as evidence_router
from app.modules.uploads.api import router as uploads_router
from app.modules.analysis.api import router as analysis_router
from app.modules.chatbot.api import router as chatbot_router
from app.modules.dashboard.api import router as dashboard_router

api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "TruthLens AI Backend is running healthy",
    }


api_router.include_router(auth_router)
api_router.include_router(claims_router)
api_router.include_router(evidence_router)
api_router.include_router(uploads_router)
api_router.include_router(analysis_router)
api_router.include_router(chatbot_router)
api_router.include_router(dashboard_router)
