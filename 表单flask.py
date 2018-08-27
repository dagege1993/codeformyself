from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'


class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	url = StringField('What is your url?', validators=[DataRequired(), URL()])
	submit = SubmitField('提交')


@app.route('/', methods=['POST', 'GET'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		url = form.url.data
		print(name, url)
		
		return redirect(url_for('add'))
	return render_template('index.html', form=form)


@app.route('/add')
def add():
	test = '<h2>金恪芝麻代理调度首页</h2><h2>获取随机代理使用函数 /代理池名/random <h2>查看代理总数使用函数 /代理池名/count</h2>' + '<h2>当前所有代理池</h2>'
	return test


if __name__ == '__main__':
	app.run()
