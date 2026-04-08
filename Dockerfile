FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .


RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

EXPOSE 7860

CMD ["python", "app.py"]