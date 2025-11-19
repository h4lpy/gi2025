FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || true

COPY quiz.py .

EXPOSE 13337

CMD ["python3", "quiz.py"]
