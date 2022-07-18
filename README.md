# Simple CRUD app with FastAPI

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple CRUD application written in FastAPI. Also it uses:
- PostgreSQL as storage
- Alembic for migrations
- SQLAlchemy as ORM
- Poetry as dependency manager
- Docker compose for building
- Black, pylint and mypy for formatting and linting

##### Easy to run locally:
```
echo DB_PASSWORD=supersecurepassword > .env
docker-compose up --build
```
