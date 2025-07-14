# 🍹 Menu Drink Selector App

A mobile-optimized web application that uses AI to analyze menu photos and randomly suggest drinks. Built with React, FastAPI, MongoDB, and Google Gemini AI.

## ✨ Features

- 📱 **Mobile-First Design**: Beautiful camera interface with viewfinder
- 🤖 **AI-Powered Analysis**: Google Gemini vision model extracts drinks from menu photos
- 🎲 **Random Selection**: Get random drink suggestions from analyzed menus
- 💾 **Data Persistence**: MongoDB stores analysis history
- 🎨 **Modern UI**: Gradient design with smooth animations
- 📸 **Camera Integration**: Native camera access for photo capture

## 🛠️ Tech Stack

- **Frontend**: React, CSS3, Camera API
- **Backend**: FastAPI, Python
- **Database**: MongoDB
- **AI**: Google Gemini (gemini-2.0-flash)
- **Integration**: emergentintegrations library

## 📋 Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- MongoDB (local or cloud)
- Google Gemini API key

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd menu-drink-selector
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env` file:
```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="menu_database"
GEMINI_API_KEY="your-gemini-api-key-here"
```

Start the backend:
```bash
python server.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

Create `frontend/.env` file:
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

Start the frontend:
```bash
npm start
```

### 4. Get Your Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `backend/.env` file

## 📱 How to Use

1. **Open the app** in your mobile browser
2. **Allow camera permissions** when prompted
3. **Position a menu** in the viewfinder
4. **Tap to capture** the menu photo
5. **Analyze menu** to extract drinks
6. **Get random suggestion** from the drinks found

## 🔧 API Endpoints

- `GET /` - Health check
- `POST /api/analyze-menu` - Analyze menu image
- `POST /api/random-drink` - Get random drink selection
- `GET /api/analysis/{id}` - Retrieve analysis by ID

## 🌐 Deployment

### Option 1: Emergent Platform
- One-click deployment
- Managed hosting
- Custom domains
- 24/7 uptime

### Option 2: Manual Deployment
- **Frontend**: Deploy to Vercel/Netlify
- **Backend**: Deploy to Railway/Heroku
- **Database**: Use MongoDB Atlas

## 📁 Project Structure

```
menu-drink-selector/
├── backend/
│   ├── server.py          # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   ├── App.css       # Styling
│   │   └── index.js      # Entry point
│   ├── package.json      # Node.js dependencies
│   └── .env             # Frontend configuration
└── README.md            # This file
```

## 🎨 Customization Ideas

- Add more AI models (OpenAI, Claude)
- Expand to food items analysis
- Implement user accounts
- Add favorites and history
- Create sharing features
- Add restaurant finder integration
- Build mobile app wrapper

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement rate limiting in production
- Add input validation and sanitization

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📞 Support

For questions or support, please create an issue in the repository.

---

Built with ❤️ using AI assistance on the Emergent platform.
