FROM python:3.9.17
MAINTAINER Robot


#将当前文件夹下面的requirements.txt复制到容器中
COPY . .

WORKDIR /code
#安装依赖
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

EXPOSE 5500

CMD gunicorn -c gunicorn.conf run:app
