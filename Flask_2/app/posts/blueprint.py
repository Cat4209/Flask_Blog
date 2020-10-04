from flask import Blueprint, render_template, redirect, url_for
from models import Post, Tag
from app import db
from flask import request

from .forms import PostForm
from flask_security import login_required

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        
        post = Post(title=title, body=body)
        
        try:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts.index'))
        except:
            return "Error Method Create"
    else:
        form = PostForm()
        return render_template('posts/create_post.html', form=form)
    

@posts.route('/<slug>/edit/', methods=["POST", "GET"])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    
    if request.method == "POST":
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        
        return redirect(url_for('posts.post_details', slug=post.slug))
    else:
        form = PostForm(obj=post)
        return render_template('posts/edit.html', post=post, form=form)

    
@posts.route('/')
def index():
    search = request.args.get('search')
    
    page = request.args.get('page')
    
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    
    if search:
        posts = Post.query.filter(Post.title.contains(search) | Post.body.contains(search))
    else:
        posts = Post.query.order_by(Post.created.desc())
        
    pages = posts.paginate(page=page, per_page=5)
    
    return render_template('posts/index.html', data=posts, pages=pages)


@posts.route('/<slug>')
def post_details(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    return render_template('posts/post_detail.html', data=post, tags=tags)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', data=posts, tag=tag)