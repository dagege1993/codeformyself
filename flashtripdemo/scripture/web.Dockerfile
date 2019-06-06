FROM registry-vpc.cn-beijing.aliyuncs.com/weegotr_com/weego_ci:crawl-scripture

EXPOSE 4010

ENTRYPOINT ["python", "-m", "web"]

COPY requirements.web.production.txt requirements.txt

RUN set -ex \
  && pip install -r requirements.txt

COPY . .
