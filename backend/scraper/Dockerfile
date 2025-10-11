FROM python:3.11-slim

RUN apt-get update \
    && apt-get -y install \
    gcc g++ git chromium

WORKDIR /app

# install python package dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add Tini
ENV TINI_VERSION=v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# import source code
COPY app /app/app

# set python path
ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]