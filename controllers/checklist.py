from flask import render_template, request

from app import app
from database.core import Session, transaction
from database.data import Item


@app.route('/all', methods=('GET',))
@transaction
def view_checklist(session):
    rows = [(x.id, x.done, x.description) for x in session.query(Item).all()]
    return render_template('checklist.html', rows=rows)


@app.route('/create', methods=('POST',))
@transaction
def create_item(session):
    i = Item()
    i.done = False
    i.description = request.form['description']
    session.add(i)
    session.commit()
    return render_template(
        'parts/checklist_item.html', id=i.id, done=False,
        description=i.description)


@app.route('/edit', methods=('POST',))
@transaction
def edit_item(session):
    i = session.query(Item).filter(Item.id == request.form['id']).first()
    i.description = request.form.get('description', i.description)
    i.done = request.form.get('done', i.done)
    return '', 204


@app.route('/remove', methods=('POST',))
@transaction
def remove_item(session):
    i = session.query(Item).filter(
        Item.id == request.form['id']).delete()
    session.commit()
    return '', 204
