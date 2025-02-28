FROM python:3.11.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

COPY .env .env

CMD alembic upgrade head; python src/main.py