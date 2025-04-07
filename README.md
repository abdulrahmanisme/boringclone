# BoringLaunch Clone

A web application for automating startup submissions to various platforms.

## Prerequisites

- Node.js (v18 or later)
- Python (v3.8 or later)
- A Supabase account and project

## Setup

### 1. Supabase Setup

1. Create a new Supabase project
2. Go to the SQL editor in your Supabase dashboard
3. Copy and paste the contents of `boringlaunch-backend/schema.sql`
4. Run the SQL to create the database schema
5. Get your project URL and anon key from Settings > API

### 2. Backend Setup

```bash
cd boringlaunch-backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit .env file and add your Supabase credentials:
# SUPABASE_URL=your_supabase_project_url
# SUPABASE_KEY=your_supabase_anon_key

# Start the backend server
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd boringlaunch-frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at http://localhost:5173
The backend API will be available at http://localhost:8000

## Features

- Add and manage startups
- Upload platform data via Excel files
- Track submission status
- Automated submission handling
- Modern UI with Tailwind CSS

## Tech Stack

- Frontend:
  - React
  - Tailwind CSS
  - React Router
  - Axios
  - React Hot Toast

- Backend:
  - FastAPI
  - Supabase
  - Selenium
  - Pandas
  - Loguru 