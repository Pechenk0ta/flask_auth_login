from flask import Flask, render_template, session, request
from db import db
from forms import Registerform, Loginform
from werkzeug.security import generate_password_hash, check_password_hash
from users import User
from sqlalchemy.exc import DataError
from flask_login import LoginManager, login_user, login_required


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
login_manager = LoginManager(app)


with app.app_context():
    db.create_all()


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = Registerform()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return('User created successfully!')
    return render_template('registerform.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/check')
def check_users():
    polz = User.query.all()
    return render_template('userscheck.html', usersq=polz)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = User.query.filter_by(username=username).first()
        except DataError:
            return ("такого пользователя не существует")
        if check_password_hash(user.password, password):
            login_user(user)
            return ("Вы успешно зашли")
        else:
            return("Пароли не совпадают")
    return render_template('loginform.html', form=form)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return ("Вы успешно вышли")


@app.route('/')
@login_required
def qwe():
    return ('qwe')

if __name__ == "__main__":
    app.run()