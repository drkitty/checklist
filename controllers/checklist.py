from flask import render_template

from app import app
from database.core import Session, transaction
from database.data import Item


@app.route('/checklist')
@transaction
def index(session):
    rows = [(x.id, x.done, x.description) for x in session.query(Item).all()]
    return render_template('checklist.html', rows=rows)
