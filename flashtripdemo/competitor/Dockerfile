FROM registry-vpc.cn-beijing.aliyuncs.com/weegotr_com/weego_ci:python

EXPOSE 4030

ENTRYPOINT ["python", "-m", "api"]

COPY requirements.txt requirements.txt

RUN set -ex \
  && pip install -r requirements.txt

COPY . .
