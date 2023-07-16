FROM python:alpine

COPY . /app
RUN pip3 install flask flask-restful
ENTRYPOINT ["python3", "/app/src/ethancedwards_api.py"]
