# Morphace Backend 

### Prerequisites

- **Python 3.9+** recommended.
- **PostgreSQL** for data storage.
- **pip** for dependency management.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/joseph8071/morphace_backend.git
2. Move to folder:
   ```bash
   cd morphace_backend
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Start the FastAPI application with Uvicorn:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
