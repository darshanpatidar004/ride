# Project Setup & Execution Instructions

This document explains how to set up, configure, and start the Ride Booking Platform.

## 1. Environment Configuration

The application relies on environment variables. A template is provided in `.env.example`.

1. Copy the example file to create your active configuration:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in the required variables:
   - **Database**: The defaults (`postgres`/`postgres`/`ride_db`) work out of the box with the provided Docker setup.
   - **JWT Authentication**: `SECRET_KEY` is pre-filled with a secure random string for development. Change this for production.
   - **APIs**: Provide your `GOOGLE_MAPS_API_KEY` for map features, and Razorpay keys for payments.

## 2. Running the Backend Infrastructure

We use Docker to easily spin up the backend API, PostgreSQL database, and Redis.

1. Ensure you have Docker and Docker Compose installed.
2. From the root of the project, run:
   ```bash
   docker-compose up --build -d
   ```
3. This will start:
   - **api**: The FastAPI application running on `http://localhost:8000`
   - **db**: PostgreSQL database running on port `5432`
   - **redis**: Redis cache running on port `6379`

### Viewing Backend Documentation
Once the containers are running, navigate to `http://localhost:8000/docs` to view the auto-generated Swagger UI for the API endpoints.

## 3. Database Migrations

The backend uses Alembic for database migrations. To initialize or apply the latest database schema:

```bash
docker exec -it ride_backend_api alembic upgrade head
```
*(Note: Migrations will be generated in upcoming phases)*

## 4. Running the Flutter Frontend

1. Ensure you have Flutter installed (`flutter doctor`).
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   flutter pub get
   ```
4. Run the application (choose your target device):
   ```bash
   flutter run
   ```

## Development Workflow

- The backend is set up with hot-reloading (`uvicorn --reload`). Changes to `/backend` files will automatically restart the server inside the Docker container.
- Flutter features hot-reloading by default during `flutter run`.
