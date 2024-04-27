FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
WORKDIR /app/
COPY requirements.txt .

RUN pip3 install -r requirements.txt
COPY . /app