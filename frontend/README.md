# Frontend - React + Vite

Modern React frontend for Tool Hub.

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

Runs at http://localhost:5173

## Build

```bash
npm run build
```

Output in `dist/` folder.

## Environment Variables

Create `.env`:

```
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── components/
│   ├── Header.jsx
│   ├── Sidebar.jsx
│   ├── ToolGrid.jsx
│   ├── ToolCard.jsx
│   └── GuideModal.jsx
├── App.jsx
├── App.css
├── main.jsx
└── index.css
```

## Customization

### Colors

Edit CSS files:
- Primary color: `#0066cc`
- Background: `#f5f5f5`

### Components

Each component has its own CSS file for easy customization.

### API Configuration

Update `API_BASE_URL` in `App.jsx` to point to your backend.
