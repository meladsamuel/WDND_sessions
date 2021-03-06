from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/sunday"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ =  "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    posts = db.relationship("Post", backref="user")
    def __repr__(self):
        return f"{self.id}.{self.name}"

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String())
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    def __repr__(self):
        return f"{self.id}.{self.body}-{self.user_id}"


@app.route("/")
def index():
    name = request.args.get("name")
    return {
        "Hello": name
    }

@app.route("/<name>")
def other_way(name):
     return {
        "Hello": name
    }

@app.route("/", methods=["POST"])
def third_way():
    body = request.get_json()
    # print(body)
    return {
        "Hello": body.get("name")
    }

@app.route("/form", methods=["POST"])
def fourth_way():
    name = request.form.get("name")
    return {
        "Hello": name
    }






















def register_user(name: str):
    new_user = User(name = name)
    db.session.add(new_user)
    db.session.commit()

def create_post(user_id: int, post_body: str):
    new_post = Post(body = post_body,  user_id = user_id)
    db.session.add(new_post)
    db.session.commit()


def get_user_by_id(id: int):
    return User.query.get(id)


def get_posts_by_user_id(id:int):
    return Post.query.filter(Post.user_id == id).all()
    

def get_posts_by_username(user_name: str):
    # return db.session.query(User, Post).join(Post).filter(User.name == user_name).all()
    new_user = User.query.filter((User.name == user_name)).first()
    return new_user.posts

def get_user_by_postid(post_id: int):
    new_post = Post.query.get(post_id)
    return new_post.user

def update_post(post_id: int, new_body: str):
    target_post  = Post.query.get(post_id)
    target_post.body = new_body
    db.session.add(target_post)
    db.session.commit()


def delete_post(post_id:int):
    new_post = Post.query.get(post_id)
    db.session.delete(new_post)
    db.session.commit()



















