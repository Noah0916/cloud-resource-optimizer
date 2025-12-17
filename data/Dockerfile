FROM python:3.12-slim

WORKDIR /app

COPY . /app

CMD ["python", "-m", "src.cloudopt_cli", "simulate", "--input", "data/resources.csv"]
