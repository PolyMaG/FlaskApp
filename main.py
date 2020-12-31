import view
from app import app, db
from comments.blueprint import comments
from posts.blueprint import posts

app.register_blueprint(posts, url_prefix="/posts")
app.register_blueprint(comments, url_prefix="/comments")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
