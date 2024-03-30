ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction
COPY . /code

ENV SECRET_KEY "O6JpVX2KQZKGy4vvFwYt5eIf1gvRq7mo8l5EL1dicCiR5Q5t6g"
RUN python manage.py collectstatic --noinput
RUN chmod +x ./startup.sh

EXPOSE 8000

#CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "agro.wsgi"]
ENTRYPOINT ["./startup.sh"]
