from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from app import db
from models import Post, Tag, Comment
from .forms import CommentForm

comments = Blueprint("comments", __name__, template_folder="templates")


@comments.route("/create", methods=["POST", "GET"])
def create_comment():
    if request.method == "POST":
        name = request.form["name"]
        body = request.form["body"]

        try:
            comment = Comment(name=name, body=body)
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            print(e)

        return redirect(url_for("comments.index"))

    form = CommentForm()
    return render_template("comments/create_comment.html", form=form)


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
        comments = Comment.query #.all()

    pages = comments.paginate(page=page, per_page=1)

    return render_template("comments/index.html", pages=pages)


@comments.route("/<slug>")
def comment_detail(slug):
    comment = Comment.query.filter(Comment.slug == slug).first()
    post = comment.post
    return render_template("comments/comment_detail.html", comment=comment, post=post)
