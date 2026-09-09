FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
COPY api/ ./api
COPY src/ ./src

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
