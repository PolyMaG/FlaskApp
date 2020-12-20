from flask import Blueprint
from flask import render_template

from models import Post, Tag, Comment

posts = Blueprint("posts", __name__, template_folder="templates")


@posts.route("/")
def index():
    posts = Post.query.all()
    return render_template("posts/index.html", posts=posts)


@posts.route("/<slug>")
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    comments = post.comments
    return render_template(
        "posts/post_detail.html", post=post, tags=tags, comments=comments
    )


@posts.route("/tag/<slug>")
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts.all()
    return render_template("posts/tag_detail.html", tag=tag, posts=posts)


@posts.route("/comments/<slug>")
def comment_detail(slug):
    comment = Comment.query.filter(Comment.slug == slug).first()
    post = comment.post
    return render_template("comments/comment_detail.html", comment=comment, post=post)
