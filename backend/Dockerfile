FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Use Gunicorn to serve the Flask app in production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
