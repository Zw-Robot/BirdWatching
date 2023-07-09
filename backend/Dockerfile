FROM python:3.9.17
MAINTAINER Robot


#将当前文件夹下面的requirements.txt复制到容器中
COPY ./requirements.txt /requirements.txt

WORKDIR /app
#安装依赖
RUN pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com


COPY . /app

EXPOSE 5500

ENTRYPOINT [ "python3" ]

CMD gunicorn -c gunicorn.conf apps:app