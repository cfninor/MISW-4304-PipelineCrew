FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --ignore-installed -r requirements.txt

COPY . .

EXPOSE 5000

ENV NEW_RELIC_CONFIG_FILE=/app/newrelic.ini

CMD ["python3", "application.py"]