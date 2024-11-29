FROM amd64/python:3.9-slim

RUN apt update && apt install -y libgomp1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

RUN pip install -U pip && \
    pip install mlflow==2.16.0 pandas scikit-learn "fastapi[all]" lightgbm

COPY . .

CMD ["uvicorn","app:app","--host","0.0.0.0","--reload"]