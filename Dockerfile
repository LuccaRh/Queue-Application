FROM python:3.11

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "backend/main.py"]