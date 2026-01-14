# Backend API Server

FastAPI backend for Tool Hub application.

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Run Development Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Tools
- `GET /api/tools` - Get all tools (with filters)
- `GET /api/tools/{id}` - Get specific tool
- `GET /api/categories` - Get all categories
- `GET /api/tags` - Get popular tags
- `GET /api/stats` - Get statistics

### Query Parameters for /api/tools
- `category` - Filter by category
- `search` - Search query
- `tags` - Comma-separated tags
- `is_external` - Filter external/internal

### Example Requests

```bash
# Get all tools
curl http://localhost:8000/api/tools

# Search tools
curl http://localhost:8000/api/tools?search=python

# Filter by category
curl http://localhost:8000/api/tools?category=development

# Get statistics
curl http://localhost:8000/api/stats
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

Create `.env` file:
```
TOOLS_CONFIG_PATH=../config/tools.yaml
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```
