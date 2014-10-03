from flask import render_template, request

from app import app
from database.core import Session, transaction
from database.data import Item


@app.route('/checklist/all', methods=('GET',))
@transaction
def view_checklist(session):
    rows = [(x.id, x.done, x.description) for x in session.query(Item).all()]
    return render_template('checklist.html', rows=rows)


@app.route('/checklist/create', methods=('POST',))
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

@app.route('/checklist/edit', methods=('POST',))
@transaction
def edit_item(session):
    i = session.query(Item).filter(id=request.form['id'])
    i.description = request.form.get('description', i.description)
    i.done = request.form.get('done', i.done)
