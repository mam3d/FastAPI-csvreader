FROM python:slim
WORKDIR /csvreader
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .