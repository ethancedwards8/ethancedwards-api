FROM python:alpine

COPY . /app
RUN pip3 install flask flask-restful
ENTRYPOINT ["python3", "/app/ethancedwards_api.py"]
