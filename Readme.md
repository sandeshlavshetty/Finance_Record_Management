# Finance Dashboard Backend API

A production-ready Django REST Framework backend for financial data management with role-based access control, advanced filtering, and comprehensive analytics.

## Quick Start

### Method 1: Test on Hosted Instance (Easiest)

**Using Swagger UI:**
1. Open the hosted backend URL and navigate to `/api/docs/`
2. Open the **Login** endpoint (`/api/auth/login/`) and click **"Try it out"**
3. Enter provided credentials and execute request:
   - Email: `admin@example.com`
   - Password: `(provided on submission)`
4. Copy the `access` token from the login response
5. Click the **"Authorize"** button (top right) and paste: `Bearer <access_token>`
6. Click **Authorize** and then test all protected endpoints

**Using Postman (Pre-configured):**
1. Open Postman → Click **"Import"** → Select files from `postman/` folder:
   - `Finance Dashboard API.postman_collection.json` (all endpoints)
   - `Finance Dashboard API.postman_environment.json` (auth variables)
2. In Postman, select the imported **Environment** from dropdown (top right)
3. Go to **Auth folder** → Click "Login" request
4. Click **"Send"** → JWT tokens should auto-save to environment variables
5. If tokens are not auto-saved, manually copy `access` and `refresh` from response and save them in the selected environment
6. Now test all other endpoints using the saved token values

### Method 2: Test Locally

**Prerequisites:**
- Python 3.9+
- PostgreSQL installed and running

**Setup Steps:**
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Create .env file in backend/ with:
SECRET_KEY=your-secret-key
DEBUG=True
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=zorvyn_db
SETUP_TOKEN=your-setup-token

# 3. Create database
createdb zorvyn_db

# 4. Run migrations
cd backend
python manage.py migrate

# 5. Initialize first admin (one-time)
python manage.py setup_admin --email admin@local.com --password admin123

# 6. Start server
python manage.py runserver
```

**Test with Postman:**
- In Postman Environment, change `base_url` to `http://localhost:8000`
- Follow same login steps as hosted instance
- All endpoints now test against your local backend

## Architecture & Key Features

**Modular Design**
- `users/` - Custom user model with email auth & role-based access (Admin, Analyst, Viewer)
- `records/` - Financial records with soft delete, audit trails, and advanced filtering
- `dashboard/` - Analytics with ORM aggregations for performance
- `core/` - Standardized response envelopes, pagination, permissions middleware

**Security & Production-Ready**
- JWT authentication at `/api/auth/login/` and `/api/auth/refresh/`
- **Setup Route** (`POST /api/users/setup/`): Securely bootstrap first admin user with:
  - Setup token validation (one-time initialization)
  - Rate limiting (5 attempts/hour/IP)
  - Audit logging on all setup attempts
- Request validation & standardized error handling
- CORS & security headers configured

**Advanced Filtering**
- Search across records by financial fields
- Filter by date range, category, transaction type
- Optimized query with select_related & prefetch_related

## Testing

**Unit Tests**
```bash
python manage.py test
```

**Coverage**: Users, Records, Dashboard, Permissions, and Edge Cases

## Deployment

Deployed on **Render** with PostgreSQL.

```bash
# Build
pip install -r backend/requirements.txt

# Run
cd backend && gunicorn config.wsgi:application
```

See `DEPLOYMENT.md` for detailed deployment steps.

## Notable Implementation Decisions

1. **Setup Route Pattern**: Addresses the chicken-egg problem of no initial admin—uses token-based security and rate limiting instead of hardcoded credentials
2. **Django/DRF Choice**: Batteries-included framework with excellent ORM, built-in permissions, and mature ecosystem for rapid, secure API development
3. **Custom User Model**: Email-based authentication for better UX than username
4. **Soft Delete**: Maintains audit trail without data loss

## Portfolio

Full-stack projects showcasing production architecture:
- **UI + Backend + AI**: Active 3000+ users, 99.9% uptime projects 
- [Portfolio](https://sandeshlavshetty.vercel.app/)