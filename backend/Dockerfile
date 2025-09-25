FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# install curl (used for healthcheck) and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# container listens on port 6000
EXPOSE 6000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6000"]
