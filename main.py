#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import Flask, g, render_template, redirect, url_for, flash, request

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

# 重设系统默认编码为utf-8
# reload(sys)
# sys.setdefaultencoding('utf8')


__all__ = ['app']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'


# CsrfProtect(app)


class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	url = StringField('What is your url?', validators=[URL()])
	submit = SubmitField('Submit')


# @app.route('/')
# def index():
#     keys = []
#     test = '<h2>金恪芝麻代理调度首页</h2><h2>获取随机代理使用函数 /代理池名/random <h2>查看代理总数使用函数 /代理池名/count</h2>' + '<h2>当前所有代理池</h2>'
#     conn = get_conn()
#     keys_list = conn.get_keys()
#     print(keys_list, type(keys_list))
#     for key in keys_list:
#         keys.append(key)
#     return test + str(keys)


@app.route('/add', methods=['GET', 'POST'])
def add():
	form = NameForm()
	
	if form.validate_on_submit():
		name = form.name.data
		url = form.url.data
		print(name, url)
		return redirect('/')
	return render_template('add_proxy.html', form=form)


# return render_template("add_proxy.html")


# @app.route('/<redis_key>/random')
# def get_proxy(redis_key):
#     """
#     Get a proxy
#     :return: 随机代理
#     """
#     conn = get_conn()
#     return conn.random(redis_key)

@app.route('/',methods=['GET', 'POST'])
def main_pqge():
	form = NameForm()
	return render_template('index.html', form=form)


# @app.route('/<redis_key>/count')
# def get_counts(redis_key):
#     """
#     Get the count of proxies
#     :return: 代理池总量
#     """
#     conn = get_conn()
#     return str(conn.count(redis_key))


# if __name__ == '__main__':
#     app.run()

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000, debug=True)
