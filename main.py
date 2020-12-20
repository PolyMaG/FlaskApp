from app import app, db
import view

from posts.blueprint import posts
from comments.blueprint import comments


app.register_blueprint(posts, url_prefix="/posts")
app.register_blueprint(comments, url_prefix="/comments")

if __name__ == "__main__":
    app.run()
