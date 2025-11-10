# Backend - Django REST Framework API

## Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
```

2. **Activate Virtual Environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create Superuser (Optional)**
```bash
python manage.py createsuperuser
```

6. **Run Development Server**
```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

## API Documentation

### Authentication Endpoints

#### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepassword"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Dataset Endpoints

All dataset endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

#### List Datasets
```http
GET /api/datasets/
```

#### Get Dataset Details
```http
GET /api/datasets/{id}/
```

#### Upload CSV
```http
POST /api/datasets/upload/
Content-Type: multipart/form-data

file: <csv_file>
```

#### Get Dataset Summary
```http
GET /api/datasets/{id}/summary/
```

#### Download PDF Report
```http
GET /api/datasets/{id}/download_pdf/
```

#### Delete Dataset
```http
DELETE /api/datasets/{id}/
```

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

Use the superuser credentials created earlier.

## Database

The project uses SQLite by default. The database file is `db.sqlite3` in the backend directory.

To reset the database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
```

## Testing

Test the API using tools like:
- Postman
- cURL
- HTTPie
- Django REST Framework browsable API at `http://localhost:8000/api/`

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### CORS Issues
Update `CORS_ALLOWED_ORIGINS` in `config/settings.py`

### Migration Issues
```bash
python manage.py makemigrations --empty api
python manage.py migrate --fake
```
