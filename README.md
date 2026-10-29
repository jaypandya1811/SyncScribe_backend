# 🚀 SyncScribe Backend

> A production-ready FastAPI backend that powers **SyncScribe**, an AI-driven meeting intelligence platform capable of transcribing multi-speaker audio, generating concise summaries, and extracting structured action items.

---

## 📖 Overview

SyncScribe automates the entire meeting documentation workflow.

Instead of manually taking notes, users upload an audio recording and the backend orchestrates a complete AI pipeline that:

* 🎙️ Uploads audio securely to AWS S3
* 📝 Transcribes conversations using Whisper Large V3
* 👥 Preserves speaker-separated dialogue
* 🤖 Generates AI-powered meeting summaries
* ✅ Extracts structured action items in strict JSON format
* 💾 Persists every processing step in PostgreSQL
* 🔄 Tracks progress through a resilient state-driven workflow

The system is designed to handle long-running AI tasks safely, allowing users to refresh the page or reconnect without losing processing progress.

---

# ✨ Features

### AI Processing

* Multi-speaker audio transcription
* AI-generated meeting summaries
* Automatic action item extraction
* Strict JSON output using openai/gpt-oss-120b

### Reliable Processing Pipeline

* State-driven workflow
* Database-backed progress persistence
* Recovery after page refreshes or network interruptions
* Graceful failure handling
* Status tracking for every processing stage

### File Management

* Secure AWS S3 uploads
* 30-day automatic lifecycle deletion
* Audio validation before processing
* Maximum upload size: **100 MB**

### File Validation

* Supported audio formats only
* Strict MIME type verification
* No dots allowed in uploaded filenames
* Minimum duration requirement
* File size validation
* Invalid upload rejection before processing begins

### Backend Architecture

* Repository-Service-Route architecture
* RESTful APIs
* Alembic database migrations
* Docker support
* Production-ready project structure

---

# 🏗️ Tech Stack

| Technology              | Purpose                |
| ----------------------- | ---------------------- |
| FastAPI                 | REST API Framework     |
| Python 3.11.4           | Backend Language       |
| Uvicorn                 | ASGI Server            |
| PostgreSQL (Supabase)   | Database               |
| SQLAlchemy              | ORM                    |
| Alembic                 | Database Migrations    |
| AWS S3                  | Audio Storage          |
| Groq Cloud API          | AI Inference           |
| Whisper Large V3        | Speech-to-Text         |
| openai/gpt-oss-120b     | Summary & Action Items |
| Docker                  | Containerization       |

---

# 🧠 Architecture

The backend follows a layered architecture to keep responsibilities separated and maintainable.

```
Client
   │
   ▼
Routes (API Layer)
   │
   ▼
Services (Business Logic)
   │
   ▼
Repositories (Database Access)
   │
   ▼
PostgreSQL
```

This separation keeps business logic independent from database operations and HTTP request handling.

---

# 🔄 Processing Workflow

```text
Upload Audio
      │
      ▼
Validate File
      │
      ▼
Store Audio in AWS S3
      │
      ▼
Create Database Record
(Status: uploaded)
      │
      ▼
Whisper Transcription
(Status: transcribed)
      │
      ▼
openai/gpt-oss-120b Summary Generation
(Status: summarized)
      │
      ▼
Extract Action Items
      │
      ▼
Completed
```

If any step fails, the backend records an appropriate failure state such as:

* transcription_failed
* summarization_failed

allowing processing status to remain transparent and recoverable.

---

# 🚀 Getting Started

## Clone the repository

```bash
git clone https://github.com/<your-username>/SyncScribe_backend.git
cd syncscribe-backend
```

---

## Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure environment variables

Create a `.env` file.

```env
DATABASE_URL=
SUPABASE_URL=
SUPABASE_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_BUCKET_NAME=
AWS_REGION=
GROQ_API_KEY=

---

## Run database migrations

```bash
alembic upgrade head
```

---

## Start the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at

```
http://localhost:8000
```

Interactive documentation:

```
http://localhost:8000/docs
```

---

# 🐳 Running with Docker

```bash
docker compose up --build
```

---

# 📌 Current Capabilities

* User management APIs
* Meeting management APIs
* Audio upload pipeline
* AWS S3 integration
* AI transcription
* AI summarization
* Action item extraction
* Jwt based authentication
* Database persistence
* Progress tracking
* Docker support
* Alembic migrations
* File validation
* Production-ready architecture

---

# 🚧 Future Improvements

* Background task queue
* WebSocket progress updates
* Email notifications
* Team collaboration
* OAuth authentication
* CI/CD pipeline
* Automated testing

---

# 🤝 Frontend Repository

The frontend for SyncScribe is maintained separately.

➡️ **Frontend Repository:** https://github.com/jaypandya1811/SyncScribe_frontend

---

# 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Jay Pandya**
pandyajay005@gmail.com

Built with **FastAPI**, **AWS**, **Supabase**, and **Groq AI** to demonstrate production-oriented backend engineering, AI integration, and scalable API design.
