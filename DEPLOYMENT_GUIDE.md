# Deployment Guide - Taking Your App Online

## Overview

This guide covers deploying all three components online:
1. **Backend** (Django API) → Railway, Render, or Heroku
2. **Web Frontend** (React) → Vercel, Netlify, or GitHub Pages
3. **Desktop App** → Distribute as executable

## Option 1: Quick Deploy (Recommended for Demo)

### Backend: Railway (Free Tier)

**Why Railway?**
- ✅ Free tier available
- ✅ Automatic PostgreSQL database
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS

**Steps:**

1. **Prepare Backend for Deployment**

Create `backend/railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && gunicorn config.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `backend/Procfile`:
```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
```

Update `backend/requirements.txt` - add:
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
dj-database-url==2.1.0
```

Update `backend/config/settings.py`:
```python
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Whitenoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS - Update with your frontend URL
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    os.getenv('FRONTEND_URL', ''),  # Add your Vercel URL here
]

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

2. **Deploy to Railway**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Link to project
railway link

# Add PostgreSQL database
railway add postgresql

# Set environment variables
railway variables set SECRET_KEY="your-secret-key-here"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="your-app.railway.app"

# Deploy
railway up
```

Or use Railway's GitHub integration:
1. Push code to GitHub
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Add PostgreSQL database
6. Set environment variables
7. Deploy!

**Your API will be at:** `https://your-app.railway.app`

### Web Frontend: Vercel (Free Tier)

**Why Vercel?**
- ✅ Free tier for personal projects
- ✅ Automatic deployments from GitHub
- ✅ Global CDN
- ✅ Automatic HTTPS

**Steps:**

1. **Update API URL**

Create `web-frontend/.env.production`:
```env
VITE_API_URL=https://your-app.railway.app/api
```

Update `web-frontend/src/lib/api.ts`:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

2. **Deploy to Vercel**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd web-frontend
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? chemical-equipment-visualizer
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

Or use Vercel's GitHub integration:
1. Push code to GitHub
2. Go to https://vercel.com
3. Click "New Project"
4. Import your repository
5. Configure:
   - Framework: Vite
   - Root Directory: web-frontend
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Add environment variable: `VITE_API_URL=https://your-app.railway.app/api`
7. Deploy!

**Your app will be at:** `https://your-app.vercel.app`

3. **Update Backend CORS**

Add your Vercel URL to Railway environment variables:
```bash
railway variables set FRONTEND_URL="https://your-app.vercel.app"
```

## Option 2: Alternative Platforms

### Backend Alternatives

#### A. Render (Free Tier)

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: chemical-equipment-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False

databases:
  - name: chemical-equipment-db
    databaseName: chemical_equipment
    user: chemical_user
```

2. Deploy:
   - Push to GitHub
   - Connect to Render
   - Automatic deployment

#### B. Heroku (Paid)

```bash
# Install Heroku CLI
heroku login

# Create app
heroku create chemical-equipment-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### Frontend Alternatives

#### A. Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd web-frontend
netlify deploy --prod

# Or use Netlify's GitHub integration
```

Create `web-frontend/netlify.toml`:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### B. GitHub Pages

```bash
# Install gh-pages
npm install --save-dev gh-pages

# Add to package.json scripts:
"predeploy": "npm run build",
"deploy": "gh-pages -d dist"

# Deploy
npm run deploy
```

Update `vite.config.ts`:
```typescript
export default defineConfig({
  base: '/chemical-equipment-visualizer/',
  // ... rest of config
})
```

## Desktop App Distribution

### Option 1: PyInstaller (Recommended)

```bash
cd desktop-app

# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name="ChemicalEquipmentVisualizer" main.py

# Executable will be in dist/ folder
```

### Option 2: Create Installer (Windows)

1. **Install Inno Setup**: https://jrsoftware.org/isinfo.php

2. Create `installer.iss`:
```iss
[Setup]
AppName=Chemical Equipment Visualizer
AppVersion=1.0
DefaultDirName={pf}\ChemicalEquipmentVisualizer
DefaultGroupName=Chemical Equipment Visualizer
OutputDir=installer
OutputBaseFilename=ChemicalEquipmentVisualizer_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\ChemicalEquipmentVisualizer.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Chemical Equipment Visualizer"; Filename: "{app}\ChemicalEquipmentVisualizer.exe"
Name: "{commondesktop}\Chemical Equipment Visualizer"; Filename: "{app}\ChemicalEquipmentVisualizer.exe"

[Run]
Filename: "{app}\ChemicalEquipmentVisualizer.exe"; Description: "Launch Chemical Equipment Visualizer"; Flags: postinstall nowait skipifsilent
```

3. Compile with Inno Setup

### Option 3: Distribute as ZIP

```bash
# Create distribution package
mkdir chemical-equipment-desktop
cp -r desktop-app/* chemical-equipment-desktop/
cp README.md chemical-equipment-desktop/

# Create requirements file
pip freeze > chemical-equipment-desktop/requirements.txt

# Zip it
zip -r chemical-equipment-desktop.zip chemical-equipment-desktop/
```

Include `INSTALL.txt`:
```
Installation Instructions:

1. Install Python 3.8 or higher
2. Extract this ZIP file
3. Open terminal in extracted folder
4. Run: pip install -r requirements.txt
5. Run: python main.py
6. Update API_URL in api_client.py to your deployed backend URL
```

## Complete Deployment Checklist

### Before Deployment

- [ ] Test everything locally
- [ ] Update API URLs in frontend
- [ ] Set DEBUG=False in production
- [ ] Generate new SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Update CORS_ALLOWED_ORIGINS
- [ ] Add production dependencies (gunicorn, psycopg2)
- [ ] Test with production database (PostgreSQL)
- [ ] Remove sensitive data from code
- [ ] Update README with deployment URLs

### Backend Deployment

- [ ] Push code to GitHub
- [ ] Create Railway/Render account
- [ ] Connect GitHub repository
- [ ] Add PostgreSQL database
- [ ] Set environment variables
- [ ] Deploy
- [ ] Run migrations
- [ ] Create superuser
- [ ] Test API endpoints
- [ ] Check logs for errors

### Frontend Deployment

- [ ] Update API URL to production
- [ ] Build locally to test
- [ ] Push to GitHub
- [ ] Create Vercel/Netlify account
- [ ] Connect GitHub repository
- [ ] Configure build settings
- [ ] Add environment variables
- [ ] Deploy
- [ ] Test all features
- [ ] Check browser console for errors

### Desktop App Distribution

- [ ] Update API_URL to production
- [ ] Test with production API
- [ ] Build executable with PyInstaller
- [ ] Test executable on clean machine
- [ ] Create installer (optional)
- [ ] Write installation instructions
- [ ] Upload to GitHub Releases or file hosting

## Environment Variables Reference

### Backend (Railway/Render)

```env
SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,your-custom-domain.com
FRONTEND_URL=https://your-app.vercel.app
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Auto-set by Railway
```

### Frontend (Vercel/Netlify)

```env
VITE_API_URL=https://your-app.railway.app/api
```

## Post-Deployment

### Monitor Your App

1. **Backend Logs**
```bash
# Railway
railway logs

# Render
# Check dashboard

# Heroku
heroku logs --tail
```

2. **Frontend Analytics**
   - Vercel Analytics (built-in)
   - Google Analytics
   - Plausible Analytics

### Set Up Custom Domain (Optional)

**Backend:**
```bash
# Railway
railway domain

# Add CNAME record: api.yourdomain.com → your-app.railway.app
```

**Frontend:**
```bash
# Vercel
vercel domains add yourdomain.com

# Add DNS records as instructed
```

### Enable HTTPS

Both Railway and Vercel provide automatic HTTPS certificates.

### Set Up Monitoring

- **Uptime monitoring**: UptimeRobot, Pingdom
- **Error tracking**: Sentry
- **Performance**: New Relic, DataDog

## Cost Estimates

### Free Tier (Perfect for Demo/Portfolio)

- **Railway**: Free $5/month credit (enough for small apps)
- **Vercel**: Free for personal projects
- **Total**: $0/month

### Paid Tier (Production)

- **Railway**: ~$10-20/month (includes PostgreSQL)
- **Vercel**: Free (or $20/month for Pro)
- **Domain**: ~$12/year
- **Total**: ~$10-20/month + domain

## Troubleshooting Deployment

### Backend Issues

**"Application Error"**
- Check logs: `railway logs`
- Verify DATABASE_URL is set
- Ensure migrations ran
- Check ALLOWED_HOSTS includes your domain

**"502 Bad Gateway"**
- Check if gunicorn is running
- Verify PORT environment variable
- Check application logs

**"Static files not loading"**
- Run `python manage.py collectstatic`
- Verify STATIC_ROOT is set
- Check whitenoise is installed

### Frontend Issues

**"API calls failing"**
- Verify VITE_API_URL is correct
- Check CORS settings in backend
- Inspect browser console for errors
- Test API directly with curl/Postman

**"404 on refresh"**
- Add redirect rules (Netlify/Vercel)
- Configure SPA routing

**"Environment variables not working"**
- Prefix with VITE_ for Vite
- Rebuild after changing env vars
- Check build logs

## Security Best Practices

1. **Never commit secrets**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use strong SECRET_KEY**
```python
import secrets
secrets.token_urlsafe(50)
```

3. **Enable security headers**
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

4. **Regular updates**
```bash
pip list --outdated
npm outdated
```

5. **Database backups**
   - Railway: Automatic backups
   - Manual: `pg_dump` for PostgreSQL

## Next Steps After Deployment

1. **Share your links**
   - Backend API: `https://your-app.railway.app`
   - Web App: `https://your-app.vercel.app`
   - Desktop App: GitHub Releases

2. **Update README**
   - Add "Live Demo" section
   - Include deployment URLs
   - Add screenshots

3. **Create demo video**
   - Record using deployed version
   - Show all features working
   - Upload to YouTube

4. **Monitor and maintain**
   - Check logs regularly
   - Monitor uptime
   - Update dependencies
   - Fix bugs as reported

## Quick Deploy Commands Summary

```bash
# Backend (Railway)
railway login
railway init
railway add postgresql
railway up

# Frontend (Vercel)
vercel login
vercel --prod

# Desktop App
pyinstaller --onefile --windowed main.py
```

---

**Congratulations!** Your app is now live and accessible from anywhere in the world! 🚀

**Demo URLs to share:**
- API: `https://your-app.railway.app/api/`
- Web App: `https://your-app.vercel.app`
- GitHub: `https://github.com/yourusername/chemical-equipment-visualizer`
