# 使用官方Python运行时作为父镜像
FROM python:3.11

RUN mkdir -p /app
# 设置工作目录
WORKDIR  /app

# 安装依赖
COPY requirements.txt /app/
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

# 复制项目文件
COPY . /app/

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb || true
RUN apt-get update
RUN apt-get install -y -f
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip
RUN mv chromedriver-linux64 web
RUN chmod +x web/chromedriver-linux64/chromedriver

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
