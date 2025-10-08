# Code Quality Monitoring Suite - Backend

Django REST API backend integrating with GitLab and SonarQube to monitor project code quality.

## Features
- Health endpoint: GET /api/health
- Projects CRUD-lite: POST /api/projects, GET /api/projects, GET /api/projects/{id}
- Trigger scan placeholder: POST /api/projects/{id}/scan
- SonarQube quality: GET /api/projects/{id}/quality
- GitLab commits: GET /api/projects/{id}/commits
- Token authentication (DRF), unauthenticated health
- Swagger docs at /docs

## Setup
1. Create and populate environment file:
   - Copy `.env.example` to `.env` (inside mcp_server_backend/)
   - Set tokens and base URLs:
     - GITLAB_BASE_URL, GITLAB_TOKEN
     - SONARQUBE_BASE_URL, SONARQUBE_TOKEN
     - DJANGO_SECRET_KEY, DJANGO_DEBUG, ALLOWED_HOSTS

2. Install dependencies:
   - pip install -r mcp_server_backend/requirements.txt

3. Apply migrations and create superuser (optional):
   - python mcp_server_backend/manage.py migrate
   - python mcp_server_backend/manage.py createsuperuser

4. Create API token:
   - python mcp_server_backend/manage.py drf_create_token <username>

5. Run server (preview system handles port):
   - python mcp_server_backend/manage.py runserver 0.0.0.0:3001

## Authentication
- Include `Authorization: Token <your-token>` header for all endpoints except `/api/health`.

## Endpoints
- GET /api/health
- POST /api/projects
- GET /api/projects
- GET /api/projects/{id}
- POST /api/projects/{id}/scan
- GET /api/projects/{id}/quality
- GET /api/projects/{id}/commits

## Notes
- Scan trigger is a placeholder; use CI sonar-scanner for real analysis.
- Ensure tokens have proper scopes to read projects and issues.
