FROM python:3.8.5-alpine

COPY . /app
WORKDIR /app
RUN pip install flask flask-restful
ENTRYPOINT ["python"]
CMD ["ethancedwards_quotes.py"]
