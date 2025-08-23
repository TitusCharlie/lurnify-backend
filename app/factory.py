# app/factory.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.courses import router as courses_router
from app.api.lessons import router as lessons_router
from app.api.modules import router as modules_router
from app.api.auth import router as auth_router
from app.api import auth, users, courses, modules, lessons, assets, publish, progress
from app.core.database import get_session, init_db

def create_app(get_session_override=None) -> FastAPI:
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # ✅ Create DB if not exists (only in dev, not during test)
        if settings.DEBUG and not get_session_override:
            settings.create_database_if_not_exists()  # <- add this line
            init_db()
        yield  # After startup, before shutdown

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0",
        lifespan=lifespan
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inject DB session override (for testing)
    if get_session_override:
        app.dependency_overrides[get_session] = get_session_override

    # Routers
    app.include_router(auth_router)
    app.include_router(courses_router)
    app.include_router(lessons_router)
    app.include_router(modules_router)
    app.include_router(assets.router, prefix="/assets", tags=["Assets"])
    app.include_router(publish.router, prefix="/courses", tags=["Publishing"])
    app.include_router(progress.router, prefix="/progress", tags=["Progress"])
    app.include_router(users.router, prefix="/users", tags=["Users"])

    return app