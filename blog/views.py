from flask import render_template

from blog import app
from .database import session
from .models import Post

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
  # Zero-indexed page
  page_index = page - 1
  
  count = session.query(Post).count()
  
  start = page_index * paginate_by
  end = start + paginate_by
  
  total_pages = (count - 1) / paginate_by + 1
  has_next = page_index < total_pages - 1
  has_prev = page_index > 0
  
  posts = session.query(Post)
  posts = posts.order_by(Post.datetime.desc())
  posts = posts[start:end]
  
  return render_template("posts.html",
                         posts=posts,
                         has_next=has_next,
                         has_prev=has_prev,
                         page=page,
                         total_pages=total_pages
                        )