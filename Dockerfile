FROM python:alpine

COPY . /app
RUN pip install flask flask-restful
ENTRYPOINT ["python", "/app/ethancedwards_quotes.py"]
