# app/factory.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.courses import router as courses_router
from app.api.lessons import router as lessons_router
from app.api.modules import router as modules_router
# from app.api.community import router as community_router
from app.api.auth import router as auth_router
from app.api import auth, users, courses, modules, lessons, publish, progress
from app.core.database import get_session, init_db
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_app(get_session_override=None) -> FastAPI:
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if settings.DEBUG and not get_session_override:
            try:
                # ✅ Try to create database if it doesn't exist (local dev only)
                conn = psycopg2.connect(
                    dbname="postgres",
                    user=settings.POSTGRES_USER,
                    password=settings.POSTGRES_PASSWORD,
                    host=settings.POSTGRES_HOST,
                    port=settings.POSTGRES_PORT,
                )
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = conn.cursor()
                cur.execute(
                    f"SELECT 1 FROM pg_database WHERE datname='{settings.POSTGRES_DB}'"
                )
                exists = cur.fetchone()
                if not exists:
                    cur.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Database check/creation skipped: {e}")

        # ✅ Always init tables (both local + Render)
        init_db()
        yield

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0",
        lifespan=lifespan
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inject DB override (for tests)
    if get_session_override:
        app.dependency_overrides[get_session] = get_session_override

    # Routers
    # Health check route (Render will hit "/")
    @app.get("/", tags=["Health"])
    def health_check():
        return {"status": "ok"}
    
    # app.include_router(community_router)
    app.include_router(auth_router)
    app.include_router(courses_router)
    app.include_router(lessons_router)
    app.include_router(modules_router)
    app.include_router(publish.router, prefix="/courses", tags=["Publishing"])
    app.include_router(progress.router, prefix="/progress", tags=["Progress"])
    app.include_router(users.router, prefix="/users", tags=["Users"])

    return app
