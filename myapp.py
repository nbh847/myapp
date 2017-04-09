#coding=utf-8

from flask import Flask, render_template, request, g, logging, redirect, \
flash, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'weassny@123123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myblog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
Bootstrap(app)

db = SQLAlchemy(app)

class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	content = db.Column(db.Text, nullable=False)
	aDate = db.Column(db.DateTime, nullable=False)

	def __repr__(self):
		return '<Article %r>' % self.title

@app.route('/login', methods=['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'weasny' and request.form['password'] == '123123':
			session['login_in'] = True
			return redirect(url_for('show_article', page=1))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('login_in', None)
	return redirect(url_for('show_article', page=1))

@app.errorhandler(404)
def page_not_found(error):
	return redirect(url_for('show_article', page=1))

@app.route('/show_article/<int:page>')
def show_article(page):
	paginate = Article.query.paginate(page, 5, False)
	article_list = paginate.items	
	return render_template('show_article.html', pagination=paginate, article_list=article_list)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
	if request.method == "POST":
		if request.form["title"]!='' and request.form["content"]!='':
			article = Article(title=request.form["title"],content=request.form["content"], aDate=datetime.now())
			db.session.add(article)
			db.session.commit()
			return redirect(url_for('show_article', page=1)) 
		else:
			flash('please fill in it')
			return redirect(url_for('add_article'))	
	return render_template('add_article.html')

@app.route('/edit_article', methods=['GET', 'POST'])
def edit_article():
        if request.method == "POST":
                if request.form["title"]!='' and request.form["content"]!='':
                        article = Article(title=request.form["title"],content=request.form["content"], aDate=datetime.now())
                        db.session.add(article)
                        db.session.commit()
                        return redirect(url_for('show_article', page=1))
                else:
                        flash('please fill in it')
                        return redirect(url_for('add_article'))
        return render_template('add_article.html')

@app.route('/admin')
def admin():
	if session['login_in'] == True:
		title_list = [{'title':i.title, 'id':i.id} for i in Article.query.all()]
		return render_template('admin.html', title_list=title_list)
	return redirect(url_for('show_article', page=1))
	
@app.route('/del_article/<int:id>')
def del_article(id):
	art = Article.query.filter(Article.id==id).first()
	db.session.delete(art)
	db.session.commit()
	return redirect(url_for('show_article', page=1))

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/test_main')
def test_main():
	return render_template('test_main.html')

if __name__ == '__main__':
	app.run()
