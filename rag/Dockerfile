FROM python:3.11.5-bookworm

# install uwsgi
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyuwsgi

# install rag
COPY ./requirements.txt /app/requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt

COPY ./requirements.extended.txt /app/requirements.extended.txt
RUN pip install -r /app/requirements.extended.txt

COPY ./app /app

COPY ./wsgi.py /

CMD ["uwsgi", "--http", "0.0.0.0:80", "--master", "-p", "4", "-w", "wsgi:app"]