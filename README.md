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


# Lurnify Backend

This is the backend MVP for **Lurnify**, a decentralized learning platform. Built with FastAPI, PostgreSQL, SQLModel, and Web3 authentication.

---

## 🛠️ Tech Stack
| Component         | Tech                         |
|------------------|------------------------------|
| Web Framework    | FastAPI                      |
| ORM              | SQLModel (SQLAlchemy-based)  |
| Database         | PostgreSQL                   |
| Auth             | Web3 JWT + OAuth             |
| Storage          | IPFS (TBD), AWS/S3 (fallback)|
| Blockchain       | web3.py                      |
| Background Tasks | Celery + Redis (TBD)         |
| Testing          | Pytest                       |

---

## 🔐 Auth Endpoints
| Method | Endpoint        | Description        |
|--------|------------------|--------------------|
| POST   | `/auth/signup`   | Register new user  |
| POST   | `/auth/login`    | Login (JWT token)  |

Auth uses JWT and supports integration with wallets (Moralis/Auth0).

---

## 📚 Course API
| Method | Endpoint                             | Description                  |
|--------|--------------------------------------|------------------------------|
| POST   | `/courses/`                          | Create a course (auth)       |
| GET    | `/courses/`                          | List all courses             |
| GET    | `/courses/{id}`                      | Get course details           |
| POST   | `/courses/{id}/contents`             | Add content to a course      |
| GET    | `/courses/{id}/contents`             | List content of a course     |

Each course is linked to content blocks (video, text, quiz, etc).

---

## 🧪 Running Tests

```bash
pytest tests/
```

Tests cover:
- Auth (signup/login)
- Course creation
- Content creation

---

## 📁 Project Structure
```
app/
├── api/            # Route handlers
├── core/           # DB, security, config
├── models/         # SQLModel ORM models
├── schemas/        # Pydantic schemas
├── tasks/          # Background task logic
├── utils/          # IPFS, helpers (TBD)
tests/              # Pytest test cases
```

---

## ✅ MVP Progress
- [x] JWT Auth (signup/login)
- [x] Course & Content CRUD
- [ ] Quiz/Test logic
- [ ] IPFS Storage Upload
- [ ] Progress Tracking
- [ ] Task Queue with Celery

> Want to contribute or extend? Pull requests welcome!
