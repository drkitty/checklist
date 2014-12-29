from uuid import uuid4

from flask import redirect, render_template, request, session

from app import app
from database.core import Session, transaction
from database.data import Item, User


def require_auth(func):
    def new_func(*args, **kwargs):
        if session.get('username', None) is None:
            return redirect('/login')
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__module__ = func.__module__
    new_func.__doc__ = func.__doc__

    return new_func


@app.route('/')
def root():
    return redirect('/all')


@app.route('/login', methods=('GET', 'POST'))
@transaction
def login(s):
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        u = s.query(User).filter(
            User.name == request.form['username']).first()
        if not u or not u.test_password(request.form['password']):
            return 'There is no user with that username and password', 403
        else:
            session['username'] = request.form['username']
            session.permanent = True
            return redirect('/all')


@app.route('/all', methods=('GET',))
@require_auth
@transaction
def view_checklist(s):
    rows = [(x.id, x.done, x.description) for x in s.query(Item).all()]
    return render_template('checklist.html', rows=rows)


@app.route('/create', methods=('POST',))
@require_auth
@transaction
def create_item(s):
    i = Item()
    i.id = uuid4().hex
    i.done = False
    i.description = request.form['description']
    s.add(i)
    s.commit()
    return render_template(
        'parts/checklist_item.html', id=i.id, done=False,
        description=i.description)


@app.route('/edit', methods=('POST',))
@require_auth
@transaction
def edit_item(s):
    i = s.query(Item).filter(Item.id == request.form['id']).first()
    i.description = request.form.get('description', i.description)
    if 'done' in request.form:
        i.done = request.form['done'] == 'true'
    return '', 204


@app.route('/remove', methods=('POST',))
@require_auth
@transaction
def remove_item(s):
    i = s.query(Item).filter(
        Item.id == request.form['id']).delete()
    s.commit()
    return '', 204
