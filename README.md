# lurnify-backend
Build and publish educational content.

# structure
project_root/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app entrypoint
│   ├── models/               # SQLModel models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── module.py
│   │   ├── lesson.py
│   │   ├── asset.py
│   │   └── progress.py
│   ├── schemas/              # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── module.py
│   │   ├── lesson.py
│   │   └── asset.py
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   ├── auth.py           # /auth/login, /auth/me
│   │   ├── users.py          # /users/{id}, /users/me/dashboard
│   │   ├── courses.py        # /courses/, /courses/{id}, /courses/generate, /courses/my
│   │   ├── modules.py        # /courses/{id}/modules/, /modules/{id}/generate
│   │   ├── lessons.py        # /modules/{id}/lessons/, /lessons/{id}
│   │   ├── assets.py         # /assets/upload, /assets/ipfs
│   │   ├── publish.py        # /courses/{id}/publish, /courses/{id}/share
│   │   └── progress.py       # /progress/{course_id}, /progress/{lesson_id}/complete
│   ├── services/             # Core logic (AI, IPFS, etc.)
│   │   ├── __init__.py
│   │   ├── ai_generator.py   # SRP: Generates outlines & content using AI
│   │   ├── ipfs.py           # SRP: Handles IPFS pinning logic
│   │   ├── auth.py           # SRP: Auth services, token management
│   │   └── storage.py        # SRP: AWS/Supabase upload logic
│   ├── tasks/                # Celery tasks (async)
│   │   ├── __init__.py
│   │   ├── video_tasks.py    # SRP: Video-related background jobs
│   │   ├── ai_tasks.py       # SRP: AI generation background jobs
│   │   └── ipfs_tasks.py     # SRP: IPFS async uploads
│   ├── core/                 # Core configs and utils
│   │   ├── __init__.py
│   │   ├── config.py         # OCP: Load from .env without changes to code
│   │   ├── database.py       # ISP: Database engine/session only
│   │   ├── dependencies.py   # DIP: Injected services for routes
│   │   └── security.py       # SRP: Auth, token, password hashing
├── celery_worker.py         # Celery entry
├── requirements.txt         # Python dependencies
├── alembic/                 # For DB migrations (optional)
├── .env                     # Environment variables
└── README.md
