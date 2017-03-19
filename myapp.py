#coding=utf-8

from flask import Flask, render_template, request, g, logging
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'weasny' and request.form['password'] == '123123':
			return render_template('login_ok.html')
	return render_template('login.html', error=error)

if __name__ == '__main__':
	app.run(debug=True)