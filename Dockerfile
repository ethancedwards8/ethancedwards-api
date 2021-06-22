FROM python:3.8.5-alpine

COPY . /app
RUN pip install flask flask-restful
ENTRYPOINT ["python", "/app/ethancedwards_quotes.py"]
