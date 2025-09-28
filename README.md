### Using alembic to connect a new database on render
1. Create postgres database on render and get the details
2. update the details in your local .env
3. connect the database external url locally to make changes to the db from your local machine
3b.Point your .env / settings to the new Render DB URL.
4. Run this to stamp the new DB as empty but synced:
    "alembic stamp head" -- This will insert a row in the new DB’s alembic_version table without running migrations.
5. Then re-run:
    "alembic upgrade head" -- That will apply all migrations from scratch on the new DB.



## API Endpoint Specifications

### Week 1 — Onboarding & Auth Module

#### POST /auth/signup

**Description:** Sign up a user via email/password or wallet

**Request Body:**

```json
{
  "email": "string",
  "username": "string (optional)",
  "password": "string (optional)",
  "wallet_address": "string (optional)"
}
```

**Response:**

```json
{
  "access_token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "username": "string",
    "wallet_address": "string",
    "auth_provider": "credentials | oauth | web3",
    "created_at": "datetime"
  }
}
```

---

#### POST /auth/login

**Description:** Login with email/password

**Request Body:**

```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**

```json
{
  "access_token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "username": "string",
    "wallet_address": "string",
    "auth_provider": "string",
    "created_at": "datetime"
  }
}
```

---

#### POST /auth/oauth

**Description:** Social login (Google, Twitter via OAuth)

**Request Body:**

```json
{
  "provider": "google | twitter",
  "token": "string"
}
```

**Response:**
Same as /auth/login

---

#### GET /users/me

**Description:** Get the current user's profile

**Headers:**

```
Authorization: Bearer <JWT>
```

**Response:**

```json
{
  "id": "string",
  "email": "string",
  "username": "string",
  "wallet_address": "string",
  "auth_provider": "string",
  "created_at": "datetime"
}
```

---

### Week 2 — Courses, Modules, Lessons, Progress

#### POST /courses/

**Description:** Create a course

**Request Body:**

```json
{
  "title": "string",
  "description": "string",
  "thumbnail_url": "string (optional)"
}
```

**Response:**

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "thumbnail_url": "string",
  "creator_id": "string",
  "is_published": false,
  "created_at": "datetime"
}
```

---

#### GET /courses/my

**Description:** Get all courses by the logged-in creator

**Response:**

```json
[
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "is_published": "boolean"
  }
]
```

---

#### POST /courses/{id}/publish

**Description:** Publish a course

**Response:**

```json
{
  "status": "published"
}
```

---

#### POST /courses/{id}/modules/

**Description:** Add module to a course

**Request Body:**

```json
{
  "title": "string"
}
```

**Response:**

```json
{
  "id": "string",
  "title": "string",
  "course_id": "string",
  "created_at": "datetime"
}
```

---

#### POST /modules/{id}/lessons/

**Description:** Add a lesson to a module

**Request Body:**

```json
{
  "title": "string",
  "content": "string (markdown)",
  "video_url": "string (optional)"
}
```

**Response:**

```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "video_url": "string",
  "module_id": "string",
  "created_at": "datetime"
}
```

---

#### POST /progress/{lesson\_id}/complete

**Description:** Mark a lesson as complete

**Response:**

```json
{
  "status": "completed",
  "lesson_id": "string"
}
```

---

#### GET /progress/{course\_id}

**Description:** Get progress in a course

**Response:**

```json
{
  "course_id": "string",
  "completed_lessons": ["string"],
  "progress_percent": "float"
}
```

---

### Week 3 — Community, Feed, Notifications

#### POST /community/

**Description:** Create a community

**Request Body:**

```json
{
  "name": "string",
  "description": "string"
}
```

**Response:**

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "datetime"
}
```

---

#### POST /community/{id}/join

**Description:** Join a community

**Response:**

```json
{
  "status": "joined",
  "community_id": "string"
}
```

---

#### GET /community/feed

**Description:** Get community feed

**Response:**

```json
[
  {
    "post_id": "string",
    "author_id": "string",
    "content": "string",
    "created_at": "datetime",
    "likes": "int"
  }
]
```

---

#### POST /community/{id}/posts

**Description:** Create a post in a community

**Request Body:**

```json
{
  "content": "string"
}
```

**Response:**

```json
{
  "post_id": "string",
  "content": "string",
  "author_id": "string",
  "created_at": "datetime"
}
```

---

#### GET /notifications/

**Description:** Get user notifications

**Response:**

```json
[
  {
    "id": "string",
    "type": "course_complete | post | milestone",
    "message": "string",
    "read": "boolean",
    "created_at": "datetime"
  }
]
```

---

#### PATCH /notifications/{id}/read

**Description:** Mark notification as read

**Response:**

```json
{
  "status": "read",
  "notification_id": "string"
}
```



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
