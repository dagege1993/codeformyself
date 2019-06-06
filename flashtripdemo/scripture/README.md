## development

### description
请使用Python3.6+, 有使用到`async/await/f-string`等新特性。
部分脚本使用了asyncio和aiohttp

### install depancies

install [splash](http://splash.readthedocs.io/en/stable/install.html)

On debian/ubuntu:
```bash
$ sudo aptitude install python3 python3-dev python3-pip python3-venv libssl-dev libxmlsec1-dev libxml2-dev
$ sudo docker run splash
$ pip install pipenv
$ ln -s scripture.Pipfile Pipfile
$ ln -s scripture.Pipfile.lock Pipfile.lock
$ pipenv install
```

On RHEL/CentOS:
```bash
$ sudo yum install python3 python3-devel python3-pip python3-venv openssl-devel libxml2-devel
$ sudo docker run splash
$ pip install pipenv
$ ln -s scripture.Pipfile Pipfile
$ ln -s scripture.Pipfile.lock Pipfile.lock
$ pipenv install
```

### start crawl
```bash
$ pipenv run scrapy crawl ustravelzoo
```

Website to be crawled:
  - https://www.travelzoo.com/?site=us
  - https://www.jetsetter.com/
  - https://www.hotels.cn/
  - https://www.hotels.com/
  - https://www.booking.com/

### Web hooks

### Dependency

``` bash
$ ln -s web.Pipfile Pipfile
$ ln -s web.Pipfile.lock Pipfile.lock
$ pipenv install
```

### Start

``` bash
$ pipenv run python -m web
```

### web单元测试

``` bash
$ python -m pytest tests/web  --cov=web --cov-report=html
```

### 可能会遇到的问题

#### 异步相关
在 `macOS High Sierra` 会报 `objc[79621]: +[__NSPlaceholderDate initialize] may have been in progress in another thread when fork() was called.`的错误，使用下面的方法解决了：

``` bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```
### Notice

#### ctfId of travelzoo:
- 0: All Deals  # Without short-trips
- 1: Hotels
- 2: Cruises  # 游轮
- 3: Vacations
- 4: Restaurants
- 5: Spas
- 6: Flights
- 7: All-Inclusive Vacations
- 8: Family-Friendly Activities
- 9: Things To Do
- 10: Luxury Trips
- 11: Advanture travel
- 12: Bus && Train
- 13: Car Rentals
- 14: Extras
- 15: Museums & Art
- 16: Activities
- 17: Entertainment
- 18: Shows, Concerts & Performances
- 19: Sporting Events
- 20: Theme Parks
- 21: Tours
- 22: Vacation Rentals
- 23: Zoos & Aquariums
- 24: City Getaways
- 25: Warm Weather Escapes
- 26: Gourmet Cuisine
- 27: Golf
- 28: Ski & Snow Sports
- 29: Water Sports & Pool Days
- 30: Air Included
- 31: Beach Resorts
- 32: Sightseeing
- 33: Cultural & Historical
- 34: Hiking & Outdoors
- 35: Luxury Spas
- 36: Luxury Dining
- 37: Kid's Entertainment
- 39: Ground Transport
- 40: Escorted
- 41: Guided Tours
- 42: Shows & Events
- 43: Dining & Lifestyle
- 44: Weekender
- 45: Short Trips  # location is needed
- 46: Car Rental & Train
- 96: Beach
- 97: Beach Vacations
- 98: All-inclusive

### 2019年4月23日 整理了 线上环境依赖
```bash
# Python version: 3.6.6

# install dependence for scripture web in production
pip install -r requirements.web.production.txt -i "https://mirrors.aliyun.com/pypi/simple/"

# install dependence for scripture task or beat in production
pip install -r requirements.task.production.txt -i "https://mirrors.aliyun.com/pypi/simple/"

# install dependence for scripture scrapy in production
pip install -r requirements.scrapy.production.txt -i "https://mirrors.aliyun.com/pypi/simple/"

# run scripture web
python -m web

# run scripture task
celery -A tasks.application worker -Q scripture -c 30 --loglevel INFO

# run scripture beat
celery -A tasks.application beat --loglevel INFO

# run scripture scrapy
scrapy crawl distributed_spider
```
