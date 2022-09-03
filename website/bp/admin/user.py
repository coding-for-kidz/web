from flask import Blueprint, request, redirect, render_template, jsonify
from werkzeug.security import generate_password_hash

from services.web.website.models.user_model import User
from services.web.website.models import database
from services.web.core.wrappers import admin_only

admin_user = Blueprint("admin_user", __name__, url_prefix="/admin-site/user/")


@admin_user.route("/")
@admin_only
def manage_users():
    all_users = User.query.all()
    return render_template("admin/admin_user.jinja", users=all_users)


@admin_user.post("/api/")
@admin_only
def admin_user_api():
    action = request.form["action"]
    if action == "create":
        user = User()
    else:
        user = User.query.filter_by(id=request.form["id"]).first()
    if user.username != "":
        user.username = request.form["username"]
    else:
        return jsonify({"status": "error", "error": "No username"})
    if request.form["password"] != "":
        user.password = generate_password_hash(
            request.form["password"], method="pbkdf2:sha512"
        )
    elif action == "create":
        return jsonify({"status": "error", "error": "No password"})
    if request.form["email"] != "":
        user.email = request.form["email"]
    if request.form["about"] != "":
        user.about = request.form["about"]
    if request.form["grade"] != "":
        user.grade = request.form["grade"]
    if request.form["admin"] != "":
        user.admin = int(request.form["admin"])
    if request.form["action"] == "create":
        database.session.add(user)
    database.session.commit()
    return jsonify({"status": "success"})


@admin_user.get("/create/")
@admin_only
def create_user():
    user = User()
    user.username = ""
    user.password = ""
    user.age = ""
    user.email = ""
    user.about = ""
    return render_template("admin/admin_user_temp.jinja", user=user, create=True)


@admin_user.get("/edit/<int:user_id>/")
@admin_only
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("admin/admin_user_temp.jinja", user=user, create=False)


@admin_user.get("/delete/<int:user_id>/")
@admin_only
def delete_user(user_id: int):
    """Deletes user"""
    user = User.query.filter_by(id=user_id).first()
    database.session.delete(user)
    database.session.commit()
    return redirect("/admin-site/users/")
