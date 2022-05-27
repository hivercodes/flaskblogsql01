from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
import requests



app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
ckeditor = CKEditor(app)
Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired()])
    #if using ckeditor, remember to change the string field you are using to the right field or it won't count as required.
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    all_posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=all_posts)

@app.route('/edit_post')
def edit_post():
    return render_template("index.html")

@app.route("/post/<int:index>")
def show_post(index):
    print(index)
    #Gets the spicific post
    requested_post = db.session.query(BlogPost).filter_by(id=int(index)).first()
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/make-post", methods=["GET", "POST"])
def make_post():
    form = CreatePostForm()
    now = datetime.now()
    month = now.strftime("%B")
    day = now.day
    year = now.year
    date = f'{month} {day}, {year}'
    if form.validate_on_submit() and request.method == "POST":
        new_post = BlogPost(title=form.title.data, subtitle=form.subtitle.data, author=form.author.data, date=date, img_url=form.img_url.data, body=form.body.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
