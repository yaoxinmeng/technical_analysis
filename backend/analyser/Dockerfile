FROM python:3.10-slim

RUN apt-get update && apt-get -y install gcc g++ git ffmpeg

WORKDIR /app

# install python package dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# import source code
COPY app /app/app

# set python path
ENV PYTHONPATH=/app

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --lifespan on