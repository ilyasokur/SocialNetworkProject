FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY pyproject.toml poetry.lock ./
#COPY migrations ./migrations
#COPY alembic.ini ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

COPY . .

EXPOSE 50051

CMD ["poetry", "run", "python", "app/main.py"]
