FROM registry-vpc.cn-beijing.aliyuncs.com/weegotr_com/weego_ci:crawl-scripture

ENTRYPOINT ["/sbin/pid1", "celery", "-A", "tasks.application"]

CMD ["worker", "-Q", "scripture", "-c", "30", "--loglevel", "INFO"]

HEALTHCHECK --interval=60s \
  --timeout=10s \
  --retries=1 \
  --start-period=5s \
  CMD sh healthcheck/celery-worker.sh

COPY requirements.task.production.txt requirements.txt

RUN set -ex \
  && pip install -r requirements.txt \
  && wget -O pid1.tar.gz \
    "https://github.com/fpco/pid1/releases/download/v0.1.2.0/pid1-0.1.2.0-linux-x86_64.tar.gz" \
  && tar -xf pid1.tar.gz \
    -C / \
  && rm -f pid1.tar.gz \
  && pid1 ls /sbin/pid1

COPY . .
