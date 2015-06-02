from flask import render_template

from blog import app
from .database import session
from .models import Post

@app.route("/")
def posts():
  posts = session.query(Post)
  posts = posts.order_by(Post.datatime.desc())
  posts = posts.all()
  return render_tempate("posts.html", posts=posts)