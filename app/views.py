# app = Flask(__name__) из __init__.py
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app import lm
from app.forms import LoginForm,EditForm
from app.models import User, ROLE_USER, ROLE_ADMIN
from datetime import datetime



@app.route('/')
@app.route('/index/')
@login_required

def index():
    # user = {'nickname': 'Andrey'} # выдуманный пользователь
    user = g.user
    posts = [ # список выдуманных постов
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'andkns'},
            'body': 'Beautiful day in Moscow!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title="home",
                           user=user,
                           posts=posts)


@lm.user_loader
def load_user(id):
    flash("load_user(id): "+str(id))
    return User.query.get(int(id))


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash("Already identificated !!!")
        return redirect(url_for('index'))

    form = LoginForm()
    '''
    Метод validate_on_submit делает весь процесс обработки. Если вы вызвали метод, когда форма будет представлена
    пользователю (т.е. перед тем, как у пользователя будет возможность ввести туда данные),
    то он вернет False, в таком случае вы знаете, что должны отрисовать шаблон.
    '''

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        flash('Login requested ="' + form.password.data + '", remember_me= ' + str(form.remember_me.data))
        check_login(form.name.data, form.password.data)
        return redirect (request.args.get('next') or url_for('index'))

    return render_template('login.html',
                           title="Логин",
                           form=form,
                           users=app.config['USER_NAMES'])

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

def check_login(name, password):

    user = User.query.filter_by(email=password).first()

    if user is None:

        user = User(nickname=name, email=password)
        db.session.add(user)
        db.session.commit()

    remember_me = False

    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember=remember_me)



@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user is None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('user.html',
        user = user,
        posts = posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500