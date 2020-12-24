from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from app import db
from models import Comment, Post, Tag

from .forms import PostForm, CommentForm


posts = Blueprint("posts", __name__, template_folder="templates")


@posts.route("/create", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            print(e)

        return redirect(url_for("posts.index"))

    form = PostForm()
    return render_template("posts/create_post.html", form=form)


@posts.route("/<slug>/edit/", methods=["POST", "GET"])
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()

    if request.method == "POST":
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for("posts.post_detail", slug=post.slug))

    form = PostForm(obj=post)
    return render_template("posts/edit_post.html", form=form, post=post)


@posts.route("/")
def index():
    search = request.args.get("search")

    page = request.args.get("page")

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if search:
        posts = Post.query.filter(
            Post.title.contains(search) | Post.body.contains(search)
        )  # .all()
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=4)

    return render_template("posts/index.html", pages=pages)


@posts.route("/<slug>")
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    comments = post.comments
    return render_template(
        "posts/post_detail.html", post=post, tags=tags, comments=comments
    )


@posts.route("/tag/<slug>")
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.all()
    return render_template("posts/tag_detail.html", tag=tag, posts=posts)


@posts.route("/<slug>/add_comment", methods=["POST", "GET"])
def create_comment(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if request.method == "POST":
        name = request.form["name"]
        body = request.form["body"]

        try:
            comment = Comment(name=name, body=body, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            print(e)

        return redirect(url_for("posts.post_detail", slug=post.slug))

    form = CommentForm()
    return render_template("posts/add_comment.html", form=form, post=post)


@posts.route("/<slug>/delete", methods=["GET", "POST"])
def delete_post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == "POST":

        try:
            db.session.delete(post)
            db.session.commit()
        except Exception as e:
            print(e)

        return redirect(url_for("posts.index"))

    return render_template("posts/delete_post.html", post=post)
