# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.11.5-bookworm

run echo "deb http://us.archive.ubuntu.com/ubuntu/ precise-updates main restricted" | tee -a /etc/apt/sources.list.d/precise-updates.list

# update packages
run apt-get update

# install required packages
run apt-get install -y sqlite3
run apt-get install -y supervisor

# add nginx stable ppa
run add-apt-repository -y ppa:nginx/stable
# update packages after adding nginx repository
run apt-get update
# install latest stable nginx
run apt-get install -y nginx

# install pip
run easy_install pip

# install uwsgi now because it takes a little while
run pip install uwsgi

# install requirement
run pip install -r /app/requirements.txt

# install our code
add ../requirements.txt /rag/requirements.txt
RUN pip install -r /rag/requirements.txt

# setup all the configfiles
run echo "daemon off;" >> /etc/nginx/nginx.conf
run rm /etc/nginx/sites-enabled/default
run ln -s /home/docker/code/nginx-app.conf /etc/nginx/sites-enabled/
run ln -s /home/docker/code/supervisor-app.conf /etc/supervisor/conf.d/


# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
run django-admin.py startproject website /home/docker/code/app/
run cd /home/docker/code/app && ./manage.py syncdb --noinput

expose 80
cmd ["supervisord", "-n"]