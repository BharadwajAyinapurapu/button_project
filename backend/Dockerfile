FROM python:3.11-slim
WORKDIR /app

COPY . .
RUN pip install --no-cache -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]