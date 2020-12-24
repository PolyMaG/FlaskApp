from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from app import db
from models import Post, Tag, Comment
from .forms import CommentForm

comments = Blueprint("comments", __name__, template_folder="templates")


@comments.route("/<slug>/edit/", methods=["POST", "GET"])
def edit_comment(slug):
    comment = Comment.query.filter(Comment.slug == slug).first_or_404()

    if request.method == "POST":
        form = CommentForm(formdata=request.form, obj=comment)
        form.populate_obj(comment)
        db.session.commit()

        return redirect(url_for("comments.comment_detail", slug=comment.slug))

    form = CommentForm(obj=comment)
    return render_template("comments/edit_comment.html", form=form, comment=comment)


@comments.route("/")
def index():
    search = request.args.get("search")

    page = request.args.get("page")

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if search:
        comments = Comment.query.filter(
            Comment.name.contains(search) | Comment.body.contains(search)
        )  # .all()
    else:
        comments = Comment.query  # .all()

    pages = comments.paginate(page=page, per_page=3)

    return render_template("comments/index.html", pages=pages)


@comments.route("/<slug>")
def comment_detail(slug):
    comment = Comment.query.filter(Comment.slug == slug).first_or_404()
    post = comment.post
    return render_template("comments/comment_detail.html", comment=comment, post=post)


@comments.route("/<slug>/delete", methods=["GET", "POST"])
def delete_comment(slug):
    comment = Comment.query.filter(Comment.slug == slug).first()
    if request.method == "POST":

        try:
            db.session.delete(comment)
            db.session.commit()
        except Exception as e:
            print(e)

        return redirect(url_for("comments.index"))

    return render_template("comments/delete_comment.html", comment=comment)
