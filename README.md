# Room Finder Backend

Room Finder is a backend system for a map-based boarding house and room finder application.
This project focuses on backend logic, data integrity, and RESTful API design using FastAPI.

The backend provides APIs for managing users, boarding houses, reviews, and inquiries.
Frontend development is handled separately.

---

##  Tech Stack

- FastAPI
- PostgreSQL (Supabase)
- SQLAlchemy (ORM)
- Pydantic (Validation)
- JWT Authentication
- Uvicorn

---

---

## ▶ How to Run (Backend)

```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload