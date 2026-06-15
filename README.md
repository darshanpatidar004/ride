# Ride Booking Platform

A complete production-grade Driver Booking Platform similar to the Quick Driver application.

## Architecture

This project is built using Clean Architecture.

- **Frontend:** Flutter (Mobile - Android/iOS, Web) using Riverpod, GoRouter, Dio.
- **Backend:** FastAPI, Python, SQLAlchemy, Alembic.
- **Database:** PostgreSQL.
- **Caching & Async:** Redis, Celery (for background tasks).
- **Real-time:** WebSockets for live driver tracking.

## Project Structure

- `/backend` - The FastAPI backend application.
- `/frontend` - The Flutter mobile and web application.
- `docker-compose.yml` - Docker compose file for running the backend, DB, and Redis locally.

## Getting Started

Please see `INSTRUCTIONS.md` for a step-by-step guide on how to set up the environment, configure keys, and run the application locally.
