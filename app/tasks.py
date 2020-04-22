import time
import sys
from rq import get_current_job
import json

from flask import render_template

from app import create_app
from app import db
from app.models import Task, User, Post
from app.email import send_email

app = create_app()
app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()

def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body': post.body,
                         'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_posts)

        # send email with data to user
        send_email('[flask webb app] Your blog posts',
                sender=app.config['ADMINS'][0], recipients=[user.email],
                text_body=render_template('email/export_posts.txt', user=user),
                html_body=render_template('email/export_posts.html', user=user),
                attachments=[('posts.json', 'application/json',
                              json.dumps({'pots': data}, indent=4))],
                sync=True)
    except:
        _set_task_progress(100)
        app.logger.error('unhandled exception', exc_info=sys.exc_info())

def water_plants(user_id, seconds):
    example(user_id,seconds)

def example(user_id, seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        _set_task_progress(100 * i // seconds)
        print(i)
        time.sleep(1)
    _set_task_progress(100)
    print('Task completed')
