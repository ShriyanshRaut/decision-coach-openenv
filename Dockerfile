FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

EXPOSE 7860

CMD ["python", "app.py"]