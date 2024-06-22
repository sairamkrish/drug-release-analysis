# gather requirements
FROM python:3.12-slim as requirements-stage
WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN apt-get update && \
    apt-get install -y git && \
    pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes


# Final stage
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]