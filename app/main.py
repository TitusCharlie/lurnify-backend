from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, users, courses, modules, lessons, assets, publish, progress

app = FastAPI(title=settings.PROJECT_NAME, version="1.0")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(modules.router, prefix="/modules", tags=["Modules"])
app.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])
app.include_router(publish.router, prefix="/courses", tags=["Publishing"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])