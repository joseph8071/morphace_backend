# Morphace Backend 

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/joseph8071/morphace_backend.git
   cd morphace_backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://username:password@hostname:5432/morphace_db
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
