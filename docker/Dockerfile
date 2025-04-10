FROM python:3.11-slim

WORKDIR /app

# Copy requirements from app directory
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application file from app directory
COPY app/app.py .

ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]