# dockerfile source: https://github.com/tiangolo/uwsgi-nginx-flask-docker/blob/master/docker-images/python3.10.dockerfile
FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY requirements.txt .
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pysqlite3-binary
COPY ./app /app