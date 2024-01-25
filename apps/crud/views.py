from apps.crud.forms import UserForm
from flask import render_template, Blueprint, redirect, url_for
from apps.app import db
from apps.crud.models import User
from flask_login import login_required

crud = Blueprint(
    'crud',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/crud'
)

@crud.route("/")
@login_required
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
@login_required
def sql():
    return "コンソールログを確認してください。"

@crud.route("/users")
@login_required
def users():
    users = User.query.all()
    return render_template("crud/index.html",users=users)


@crud.route("/users/new",methods=["GET","POST"])
@login_required
def create_user():
    form = UserForm()
    username = form.username.data
    email = form.email.data
    password = form.password.data
    if form.validate_on_submit():
        user = User(
            username = username,
            email = email,
            password = password
        )
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))
    return render_template("crud/create.html",form=form)

@crud.route("/users/<user_id>", methods=["GET","POST"])
@login_required
def edit_user(user_id):
    form = UserForm()

    # 更新前のuserを取得
    user = User.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    return render_template("crud/edit.html", form=form, user=user)

@crud.route("/users/delete/<user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    #削除前のuserを取得
    user = User.query.filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("crud.users"))