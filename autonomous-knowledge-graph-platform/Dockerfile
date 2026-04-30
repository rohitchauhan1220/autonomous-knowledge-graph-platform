FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "-c", "deployment/gunicorn/gunicorn.conf.py", "backend.wsgi:app"]
