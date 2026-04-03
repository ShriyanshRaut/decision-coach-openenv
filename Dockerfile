# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies (IMPORTANT FIX HERE)
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]