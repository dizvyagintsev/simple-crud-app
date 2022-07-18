FROM python:3.10

WORKDIR /code

# Install poetry:
RUN pip install "poetry==1.1.4"

# Disable virtualenv creation:
RUN poetry config virtualenvs.create false

# Copy requirements and alembic:
COPY ./pyproject.toml ./poetry.lock* /code/
COPY ./alembic.ini /code/
COPY ./alembic /code/alembic

# Install deps:
RUN poetry install --no-root

COPY ./app /code/app