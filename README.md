# Tool Hub - React Frontend + FastAPI Backend

Modern, scalable tool hub with separated frontend and backend.

## 📁 Project Structure

```
Website/
├── backend/           # FastAPI backend
│   ├── main.py       # API server
│   └── requirements.txt
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── src/              # Shared Python code
│   ├── models/
│   ├── services/
│   └── config/
└── config/           # Configuration files
    └── tools.yaml
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18+) - [Download](https://nodejs.org/)
- **Python** (3.9+)

### 1. Start Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs at: **http://localhost:8000**  
API docs: **http://localhost:8000/docs**

### 2. Start Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: **http://localhost:5173**

## 🎨 Features

### Frontend
- ✅ Modern React with Vite
- ✅ Component-based architecture
- ✅ Responsive design
- ✅ Real-time search & filtering
- ✅ Beautiful UI with animations
- ✅ Modal guide viewer with ESC support
- ✅ Easy CSS customization

### Backend
- ✅ FastAPI - Fast & modern
- ✅ RESTful API
- ✅ Auto documentation (Swagger)
- ✅ CORS enabled
- ✅ Reusable services layer

## 📝 Adding New Tools

Edit `config/tools.yaml`:

```yaml
tools:
  - id: my-tool
    name: My Tool
    description: Tool description
    category: development
    icon: 🔧
    url: https://example.com
    tags: [tag1, tag2]
    is_external: true
    guide_content: |
      # Usage Guide
      Your guide here...
```

## 🌐 Deployment

### Backend Deployment

**Render / Railway / Heroku:**
```bash
cd backend
# Connect to platform and deploy
```

**Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment

**Vercel (Recommended):**
```bash
cd frontend
npm run build
vercel --prod
```

**Netlify:**
```bash
cd frontend
npm run build
# Upload dist/ to Netlify
```

## 🛠️ Development Tips

### Hot Reload
Both frontend and backend support hot reload in dev mode.

### API Proxy
Frontend proxies `/api` to backend automatically via Vite config.

### Debugging
- Backend: Check http://localhost:8000/docs
- Frontend: React DevTools in browser

## 📚 API Endpoints

### Tools
- `GET /api/tools` - Get all tools (with filters)
- `GET /api/tools/{id}` - Get specific tool
- `GET /api/categories` - Get categories
- `GET /api/tags` - Get popular tags
- `GET /api/stats` - Get statistics

### Example Request
```bash
curl "http://localhost:8000/api/tools?category=development&search=python"
```

## 🎨 Customization

### Change Colors
Edit CSS files in `frontend/src/components/`

Main colors:
- Primary: `#0066cc` → Change to your brand color
- Background: `#f5f5f5`
- Text: `#333`

### Add Features
1. **Backend**: Add endpoints in `backend/main.py`
2. **Frontend**: Create components in `frontend/src/components/`

## 📦 Tech Stack

**Frontend:**
- React 18
- Vite
- Axios
- CSS3

**Backend:**
- FastAPI
- Uvicorn
- Pydantic
- PyYAML

## Why This Architecture?

**Streamlit limitations:**
- ❌ Hard to customize UI
- ❌ Limited styling options
- ❌ Not suitable for public-facing apps

**React + FastAPI benefits:**
- ✅ Complete UI control
- ✅ Modern, fast frontend
- ✅ Scalable backend
- ✅ Easy deployment
- ✅ Professional look & feel

---

**Built with ❤️ using React + FastAPI**
