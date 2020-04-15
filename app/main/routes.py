#----------------------- LIB ----------------------#
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import get_locale, _

from werkzeug.urls import url_parse
from datetime import datetime
from guess_language import guess_language

#------------------------ APP ---------------------#
from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.plant import startWatering
from app.models import User, Post
from app.translate import translate
from app.main import bp

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())

#################### MAIN MENY ROUTES ######################
@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/forum", methods=['GET', 'POST'])
@login_required
def forum():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.forum'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page,
                                                   current_app.config['POSTS_PER_PAGE'],
                                                   False)
    next_url = url_for('main.forum', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.forum', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("forum.html", title='Forum', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page,
                                                   current_app.config['POSTS_PER_PAGE'],
                                                   False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("forum.html", title='Explore',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

########################### USERS  ##################################
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page,
                                               current_app.config['POSTS_PER_PAGE'],
                                               False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username) not found.', username=username))
        return redirect(url_for('main.home'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)!', username=username))
    return redirect(url_for('main.user', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username) not found.', username=username))
        return redirect(url_for('main.home'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    curent_user.unfollow(user)
    db.session.commit()
    flash(_('You are not folling %(username).', username=username))
    return redirect(url_for('main.user', username=username))

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)

########################### Search #################################
@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                                current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, pate=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                            next_url=next_url, prev_url=prev_url)

########################### WATERING APP ############################
ButtonPressed = 0
@bp.route("/plants", methods=['GET', 'POST'])
@login_required
def plants():
    global ButtonPressed
    if request.method == "POST":
        ButtonPressed += 1
        return(redirect(url_for("water")))
    return render_template("plants.html", Button = ButtonPressed)

@bp.route("/water")
@login_required
def water():
    startWatering()
    return(redirect(url_for('main.plants')))

################# TRANSLATE     ################################
@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})

################# HIDDEN ROUTES ################################
@bp.route("/robert")
def robert():
    return "Hello, Robert!"

@bp.route("/cathrine")
def cathrine():
    return "Tack så mycket Cathrine!"