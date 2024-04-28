FROM tiangolo/uwsgi-nginx-flask:python3.11

# before you are able to compile, you need to install the linux C compiler.
RUN apt-get update
RUN apt-get install build-essential


# require higher sqlite version
RUN apt-get install libreadline-dev
RUN apt-get install --upgrade sqlite3 -y
RUN wget https://sqlite.org/2021/sqlite-autoconf-3350100.tar.gz
RUN tar -xvf sqlite-autoconf-3350100.tar.gz && cd sqlite-autoconf-3350100 && ./configure
# RUN ls
RUN cd /app/sqlite-autoconf-3350100 && make
RUN apt-get purge sqlite3 -y
RUN cd /app/sqlite-autoconf-3350100 && make install

# install rag
COPY ./requirements.txt /app/requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt

COPY ./app /app
# Copy nginx conf, see base dockerfile's entrypoint.sh
COPY ./nginx.conf /app/nginx.conf
# CMD ["bash"]