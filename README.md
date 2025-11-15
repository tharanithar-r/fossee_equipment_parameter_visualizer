# Chemical Equipment Parameter Visualizer

A full-stack application for visualizing and analyzing chemical equipment data with both web and desktop interfaces. Upload CSV files containing equipment parameters and get instant analytics with interactive charts, statistics, and PDF reports.

## Features

### Core Functionality
- **CSV Data Upload** - Import equipment data with parameters (Name, Type, Flowrate, Pressure, Temperature)
- **Interactive Visualizations** - Pie charts with percentage labels and grouped bar charts
- **Real-time Analytics** - Automatic calculation of averages, min/max values, and type distribution
- **Dataset Management** - Store and manage up to 5 datasets per user with dropdown selection
- **PDF Report Generation** - Download comprehensive reports with charts and data tables
- **Sortable Data Tables** - Client-side sorting and pagination for equipment details

### User Experience
- **JWT Authentication** - Secure token-based user authentication
- **Theme Toggle** - Light/dark mode support in both web and desktop apps
- **Dual Interface** - Access via modern web browser or native desktop application
- **Responsive Design** - Web interface works on desktop, tablet, and mobile devices
- **CSV Validation** - Automatic validation with detailed error messages

## Tech Stack

### Backend
- **Django 5.0** + **Django REST Framework** - RESTful API server
- **JWT** - Token-based authentication
- **Pandas** - CSV parsing and data analytics
- **ReportLab** - PDF report generation
- **SQLite** - Database for development and production

### Web Frontend
- **React 19** + **TypeScript** - Modern web framework
- **Vite** - Fast build tool and dev server
- **shadcn/ui** - Beautiful UI components
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Interactive data visualizations
- **TanStack Table** - Advanced table features
- **Axios** - HTTP client for API calls

### Desktop Application
- **PyQt5** - Native desktop GUI framework
- **Matplotlib** - Chart rendering
- **Requests** - HTTP client for API communication

## Project Structure

```
chemical-visualizer/
├── backend/                    # Django REST API
│   ├── api/                   # Main API application
│   │   ├── models.py         # Dataset and Equipment models
│   │   ├── views.py          # API endpoints
│   │   ├── serializers.py    # Data serialization
│   │   └── utils.py          # PDF generation utilities
│   ├── config/               # Django configuration
│   │   ├── settings.py       # Project settings
│   │   └── urls.py           # URL routing
│   ├── manage.py
│   └── requirements.txt
│
├── web-frontend/              # React web application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── contexts/         # React contexts (Auth, Theme)
│   │   ├── lib/              # Utilities and API client
│   │   ├── pages/            # Page components
│   │   └── main.tsx          # Application entry point
│   ├── package.json
│   └── vite.config.ts
│
├── desktop-app/               # PyQt5 desktop application
│   ├── main.py               # Application entry point
│   ├── auth_window.py        # Login/Register window
│   ├── main_window.py        # Main application window
│   ├── api_client.py         # API communication
│   ├── theme_manager.py      # Theme management
│   └── requirements.txt
│
└── README.md
```

## Prerequisites

- **Python** 3.8 or higher
- **Node.js** 16 or higher
- **npm** or **yarn**
- **pip** (Python package manager)

## Installation & Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database tables
python manage.py makemigrations
python manage.py migrate

# (optional) Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Backend runs on:** `http://localhost:8000`

### 2. Web Frontend Setup

```bash
# Navigate to web frontend directory
cd web-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Web app runs on:** `http://localhost:5173`

### 3. Desktop Application Setup

```bash
# Navigate to desktop app directory
cd desktop-app

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## Usage Guide

### Web Application

1. **Access** - Open `http://localhost:5173` in your browser
2. **Register** - Create a new account or login with existing credentials
3. **Upload Data** - Click "Upload CSV" and select your equipment data file
4. **Select Dataset** - Choose from your uploaded datasets using the dropdown
5. **Analyze** - View interactive pie and bar charts with statistics
6. **Sort & Filter** - Click column headers in the data table to sort
7. **Download Report** - Click "Download PDF" to generate a comprehensive report
8. **Toggle Theme** - Use the sun/moon icon to switch between light and dark modes

### Desktop Application

1. **Launch** - Run `python main.py` from the desktop-app directory
2. **Login** - Enter your credentials or register a new account
3. **Upload** - Click "Upload CSV" button to import data
4. **Select Dataset** - Choose from the dropdown menu
5. **View Charts** - See pie and bar charts with your data
6. **Browse Table** - Scroll through the equipment details table
7. **Download PDF** - Click "Download PDF" to save a report
8. **Toggle Theme** - Click the theme button (Light/Dark)

### CSV File Format

Your CSV file must include these exact column headers:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,25.3,180.2
Heat Exchanger-B2,Heat Exchanger,200.8,15.7,120.5
Pump-C3,Pump,180.2,30.1,95.8
```

**Requirements:**
- Column names must match exactly (case-sensitive)
- Flowrate, Pressure, and Temperature must be numeric values
- Empty rows will be automatically removed

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and receive JWT tokens |
| POST | `/api/auth/refresh/` | Refresh access token |

### Datasets
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/datasets/` | List user's datasets (last 5) |
| GET | `/api/datasets/{id}/` | Get dataset details with equipment |
| POST | `/api/datasets/upload/` | Upload new CSV file |
| DELETE | `/api/datasets/{id}/` | Delete dataset |
| GET | `/api/datasets/{id}/summary/` | Get statistics and type distribution |
| GET | `/api/datasets/{id}/download_pdf/` | Download PDF report |

**Authentication:** All dataset endpoints require JWT token in Authorization header:
```
Authorization: Bearer <access_token>
```

## Key Features Explained

### Data Visualization
- **Pie Chart** - Shows equipment type distribution with percentage labels on each slice
- **Bar Chart** - Displays average, minimum, and maximum values for each parameter
- **Interactive** - Click legend items to show/hide data series
- **Theme-Aware** - Charts adapt colors based on light/dark theme

### Dataset Management
- **Auto-Limit** - System keeps only the 5 most recent datasets per user
- **Auto-Cleanup** - Older datasets are automatically deleted when limit is exceeded
- **Quick Selection** - Dropdown shows dataset name, upload date, and item count

### Data Table Features
- **Sortable Columns** - Click any column header to sort ascending/descending
- **Pagination** - Navigate through large datasets with Previous/Next buttons
- **Responsive** - Table adapts to different screen sizes

### PDF Reports
- **Comprehensive** - Includes all charts, statistics, and data tables
- **Professional** - Clean layout with proper formatting
- **Downloadable** - Save reports for offline viewing or sharing

## Configuration

### Backend Configuration

Edit `backend/config/settings.py` to customize:

```python
# CORS settings for web frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Add your frontend URL
]

# JWT token expiration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Dataset limit per user
MAX_DATASETS_PER_USER = 5  # Change in views.py
```

### Frontend Configuration

Edit `web-frontend/src/lib/api.ts` to change API URL:

```typescript
const API_BASE_URL = 'http://localhost:8000/api';
```

### Desktop App Configuration

Edit `desktop-app/api_client.py` to change API URL:

```python
self.base_url = 'http://localhost:8000/api'
```

## Building for Production

### Web Frontend

```bash
cd web-frontend

# Build for production
npm run build

# Output will be in dist/ folder
# Deploy dist/ folder to your web server
```

### Desktop Application

```bash
cd desktop-app

# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile --windowed --name ChemicalVisualizer main.py

# Executable will be in dist/ folder
```

### Backend Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Set up a reverse proxy (Nginx, Apache)
5. Use environment variables for secrets
6. Consider PostgreSQL or MySQL for production database