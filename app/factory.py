# app/factory.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.courses import router as courses_router
from app.api import auth, users, courses, modules, lessons, assets, publish, progress
from app.core.database import get_session, init_db

def create_app(get_session_override=None) -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Run only in development mode and not during testing
        if settings.DEBUG and not get_session_override:
            init_db()
        yield  # After startup, before shutdown

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0",
        lifespan=lifespan  #  Modern startup hook
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
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(courses_router)
    # app.include_router(courses.router, prefix="/courses", tags=["Courses"])
    app.include_router(modules.router, prefix="/modules", tags=["Modules"])
    app.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])
    app.include_router(assets.router, prefix="/assets", tags=["Assets"])
    app.include_router(publish.router, prefix="/courses", tags=["Publishing"])
    app.include_router(progress.router, prefix="/progress", tags=["Progress"])

    return app