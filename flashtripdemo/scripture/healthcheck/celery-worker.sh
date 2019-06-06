
pipenv \
    run \
    celery \
    -A tasks.application \
    inspect \
    ping \
    -d "celery@$HOSTNAME" > /dev/null 2>&1
if [ $? != 0 ]; then
    ps aux | grep 'celery' | grep 'worker' | awk '{print $2}' | xargs kill -9
    exit 1
fi
