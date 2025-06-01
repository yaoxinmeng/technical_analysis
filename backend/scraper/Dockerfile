FROM python:3.10-slim

RUN apt-get update && apt-get -y install gcc g++ git xvfb

WORKDIR /app

# install python package dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright for scraping
RUN playwright install chromium
RUN playwright install-deps

# import source code
COPY app /app/app
COPY scripts /app/scripts

# set python path
ENV PYTHONPATH=/app

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --lifespan on