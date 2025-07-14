# Setup Instructions

## Required Environment Variables

### Backend (.env)
```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="menu_database"
GEMINI_API_KEY="your-gemini-api-key-here"
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

## Installation & Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python server.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Getting Your Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your backend/.env file

## Emergency Integration Install

If you get import errors for emergentintegrations:

```bash
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```