from apps.crud.forms import UserForm
from apps.auth.forms import SignUpForm, LoginForm
from flask import render_template, Blueprint, redirect, flash, url_for, request
from apps.app import db
from apps.crud.models import User
from flask_login import login_user, logout_user

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/auth'
)

@auth.route("/")
def index():
    return render_template("auth/index.html")

@auth.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )

        if user.is_duplicated_email():
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("auth.signup"))
        
        db.session.add(user)
        db.session.commit()

        login_user(user)

        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("crud.users")
        return redirect(next_)
    
    return render_template("auth/signup.html", form=form)

@auth.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("crud.users"))
        
        flash("メールアドレスまたはパスワードが不正です")

    return render_template("auth/login.html", form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))