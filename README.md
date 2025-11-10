# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for visualizing and analyzing chemical equipment data. Built with Django REST Framework backend, React web frontend, and PyQt5 desktop application.

## Features

- **CSV Upload**: Upload chemical equipment data with parameters (Equipment Name, Type, Flowrate, Pressure, Temperature)
- **Data Visualization**: Interactive charts showing equipment type distribution and parameter statistics
- **Summary Analytics**: Automatic calculation of averages, min/max values
- **Dataset History**: Store and manage last 5 uploaded datasets
- **PDF Reports**: Generate and download comprehensive PDF reports
- **JWT Authentication**: Secure user authentication with token-based system
- **Dark Mode**: Toggle between light and dark themes (Web only)
- **Dual Interface**: Access via modern web browser or desktop application

## Project Structure

```
.
├── backend/                 # Django REST Framework API
│   ├── api/                # Main API app
│   ├── config/             # Django settings
│   ├── manage.py
│   └── requirements.txt
├── web-frontend/           # React + TypeScript web app
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── desktop-app/            # PyQt5 desktop application
│   ├── main.py
│   ├── auth_window.py
│   ├── main_window.py
│   ├── api_client.py
│   └── requirements.txt
├── sample_data/            # Sample CSV files
│   └── sample_equipment_data.csv
└── README.md
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend (Web) | React.js + TypeScript + shadcn/ui + Chart.js | Modern web interface with charts |
| Frontend (Desktop) | PyQt5 + Matplotlib | Desktop application with embedded charts |
| Backend | Django + Django REST Framework | RESTful API server |
| Authentication | JWT (Simple JWT) | Secure token-based auth |
| Data Processing | Pandas | CSV parsing and analytics |
| Database | SQLite | Store datasets and user data |
| PDF Generation | ReportLab | Generate PDF reports |

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Backend will run on `http://localhost:8000`

### 2. Web Frontend Setup

```bash
cd web-frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Web app will run on `http://localhost:5173`

### 3. Desktop App Setup

```bash
cd desktop-app

# Create virtual environment (if not using backend's venv)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## Usage

### Web Application

1. Open `http://localhost:5173` in your browser
2. Register a new account or login
3. Upload a CSV file with equipment data
4. View interactive charts and statistics
5. Download PDF reports
6. Toggle dark mode using the moon/sun icon

### Desktop Application

1. Run `python main.py` from the desktop-app directory
2. Login or register an account
3. Upload CSV files using the "Upload CSV" button
4. Select datasets from the dropdown
5. View charts and data table
6. Download PDF reports

### CSV Format

Your CSV file should have the following columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,25.3,180.2
Heat Exchanger-B2,Heat Exchanger,200.8,15.7,120.5
```

Sample data is provided in `sample_data/sample_equipment_data.csv`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/refresh/` - Refresh access token

### Datasets
- `GET /api/datasets/` - List all datasets (last 5)
- `GET /api/datasets/{id}/` - Get dataset details
- `POST /api/datasets/upload/` - Upload new CSV file
- `DELETE /api/datasets/{id}/` - Delete dataset
- `GET /api/datasets/{id}/summary/` - Get dataset summary with statistics
- `GET /api/datasets/{id}/download_pdf/` - Download PDF report

## Features Highlights

### Web Frontend
- **Modern UI**: Built with shadcn/ui components and Tailwind CSS
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode**: Persistent theme preference
- **Interactive Charts**: Using Chart.js for beautiful visualizations
- **Real-time Updates**: Automatic refresh after uploads

### Desktop Application
- **Native Feel**: PyQt5 provides native OS integration
- **Embedded Charts**: Matplotlib charts directly in the application
- **File Dialogs**: Native file picker for CSV and PDF
- **Offline Capable**: Works with local backend instance

## Security

- JWT-based authentication
- Password hashing with Django's built-in system
- CORS configuration for web frontend
- Token refresh mechanism
- Protected API endpoints

## Data Management

- Automatically stores last 5 datasets per user
- Older datasets are automatically deleted
- CSV validation on upload
- Data cleaning (removes null values)
- Efficient bulk insert for equipment records

## Troubleshooting

### Backend Issues
- **Port already in use**: Change port with `python manage.py runserver 8001`
- **Database errors**: Delete `db.sqlite3` and run migrations again
- **CORS errors**: Check `CORS_ALLOWED_ORIGINS` in `settings.py`

### Frontend Issues
- **Module not found**: Run `npm install` again
- **API connection failed**: Ensure backend is running on port 8000
- **Build errors**: Clear node_modules and reinstall

### Desktop App Issues
- **PyQt5 installation fails**: Try `pip install PyQt5-sip` first
- **Matplotlib errors**: Install with `pip install matplotlib --upgrade`
- **Connection refused**: Ensure backend is running

## Building for Production

### Web Frontend
```bash
cd web-frontend
npm run build
# Output in dist/ folder
```

### Desktop App
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py
```
