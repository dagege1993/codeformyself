FROM registry-vpc.cn-beijing.aliyuncs.com/weegotr_com/weego_ci:crawl-scripture

ENTRYPOINT ["scrapy", "crawl", "distributed_spider"]

COPY requirements.web.production.txt requirements.txt

RUN set -ex \
  && pip install -r requirements.txt

COPY . .
