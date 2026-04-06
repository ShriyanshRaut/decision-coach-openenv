FROM python:3.10-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs appear instantly
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

# Upgrade pip first (cleaner installs)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

EXPOSE 7860

CMD ["python", "app.py"]