from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///justcraft.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#==============Класс Новостей================
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<News %r>' % self.id

#==============Класс Пользователя================


#==========Логин================


#==========Главная страница================
@app.route('/')
@app.route('/main')
def index():
    return render_template('index.html')

#==========Создать новость================
@app.route('/create_news', methods=['POST', 'GET'])
def create_news():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        news = News(title=title, text=text)

        try:
            db.session.add(news)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Ошибка'
    else:
        return render_template('create_news.html')

#==========Все новости================
@app.route('/posts')
def posts():
    news = News.query.order_by(News.date.desc()).all()
    return render_template('posts.html', news=news)

#==========Читать новость================
@app.route('/posts/<int:id>')
def post_detail(id):
    new = News.query.get(id)
    return render_template('post_detail.html', new=new)

#==========Удалить новость================
@app.route('/posts/<int:id>/delete')
def post_delete(id):
    new = News.query.get_or_404(id)

    try:
        db.session.delete(new)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Ошибка'

#==========Редактировать новость================
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    new = News.query.get(id)
    if request.method == 'POST':
        new.title = request.form['title']
        new.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Ошибка'
    else:
        return render_template('post_update.html', new=new)

#==========Страница не найдена================
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#==========Про нас================
@app.route('/about')
def about():
    return render_template('about.html')

#==========Купить аккаунт================
@app.route('/accounts')
def accounts():
    return render_template('accounts.html')

#==========Профиль================
@app.route('/profile')
def profile():
    return render_template('profile.html')

#==========Магазин================
@app.route('/shop')
def shop():
    return render_template('shop.html')

#==========Форум================
@app.route('/board')
def board():
    return render_template('board.html')

#==========Пользователь================
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'User: ' + str(name) + ' - ' + str(id)

#========================================
if __name__ == '__main__':
    app.run(debug = True) #Показывать ошибки