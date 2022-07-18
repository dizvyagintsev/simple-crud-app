# Simple CRUD app with FastAPI

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![CI workflow](https://github.com/dizvyagintsev/simple-crud-app/actions/workflows/ci.yml/badge.svg)

Simple CRUD application built with FastAPI. Also it uses:
- PostgreSQL as storage
- Alembic for migrations
- SQLAlchemy as ORM
- Poetry as a dependency manager
- Docker compose for building
- Black, pylint and mypy for formatting and linting
- PyTest for testing
- Gihub Actions for CI

##### Easy to run locally:
```
echo DB_PASSWORD=supersecurepassword > .env
docker-compose up --build
```

##### Tests:
Tests divided on unit (mocks DAL) and integration (uses real database)
- Run unit tests: `pytest`
- Run integration tests:
```
echo DB_PASSWORD=supersecurepassword > .env
docker-compose run web bash -c "alembic upgrade head && pytest app --integration"
```
