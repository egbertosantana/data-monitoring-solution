FROM python:3.12

ENV PYTHONPATH=/app
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD ["flask", "run", "-h", "0.0.0.0"]