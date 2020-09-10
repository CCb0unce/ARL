FROM centos:7

WORKDIR /code

RUN yum install epel-release python36  fontconfig wqy-microhei-fonts -y

RUN python3.6 -m ensurepip --default-pip

RUN pip3.6 install pip --upgrade

RUN rpm -vhU https://nmap.org/dist/nmap-7.80-1.x86_64.rpm

RUN yum install python36-devel gcc-c++ -y

RUN yum install nginx -y

COPY app/ app/

RUN ln -s /code/app/tools/phantomjs  /usr/bin/phantomjs

COPY docker/frontend/ frontend/

COPY docker/nginx.conf  /etc/nginx/nginx.conf

COPY requirements.txt requirements.txt

#RUN pip3.6 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY docker/GeoLite2/ /data/GeoLite2/

RUN pip3.6 install -r requirements.txt



