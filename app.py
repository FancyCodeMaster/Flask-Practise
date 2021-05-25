# Importing flask
from flask import Flask , render_template , request , redirect

from datetime import datetime

# Importing SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


# Creating object named app
app = Flask(__name__)


# First Routing to the localhost
@app.route("/")
@app.route("/index")
def initial():
    return render_template("index.html")


# Configuring where our database stays
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///check.db"

# creating our database
db = SQLAlchemy(app)

# Creating flask models
# for flask models we create where we inherit from db.Model inside which we define our columns

class Post(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100) , nullable=False)
    content = db.Column(db.Text , nullable = False)
    author = db.Column(db.String(20) , nullable = False , default = "N/A")
    date_created = db.Column(db.DateTime , nullable = False , default = datetime.utcnow)

    # repr method will be called and its returned value will be shown whenever we call query.all() from the object of model class
    def __repr__(self):
        return "Post"+str(self.id)

# to construct our database , we have to import database from app and run create_all() from that db

# Now getting values from the posts.html and adding to the database and showing it in the same page
@app.route("/posts" , methods=["GET" , "POST"])
def post_show():
    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["content"]
        post_author = request.form["author"]
        post = Post(title=post_title , content = post_content , author = post_author)
        db.session.add(post)
        db.session.commit()
        return redirect("/posts")
    else:
        posts = Post.query.all()
        return render_template("posts.html" , post = posts)

# Deleting a post from the button
@app.route("/posts/delete/<int:id>")
def post_delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

# Editing a post 
@app.route("/posts/edit/<int:id>" , methods=["GET" , "POST"])
def post_edit(id):
    post = Post.query.get(id)
    if request.method == "POST":
        new_title = request.form["title"]
        new_content = request.form["content"]
        new_author = request.form["author"]

        if new_title:
            post.title = new_title
        if new_content:
            post.content = new_content
        if new_author:
            post.author = new_author
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("edit.html" , newpost = post)





# Run the app if __name__ == "__main__" , meaning it is run as the main program
if __name__ == "__main__":
    app.run(debug = True)