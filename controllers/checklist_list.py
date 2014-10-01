from flask import render_template

from app import app


@app.route('/checklist')
def index():
    return render_template('checklist_list.html', rows=[
        (2, True, 'Task 1'),
        (5, False, 'Task 2'),
        (11, False, 'Task 3 (longer)'),
    ])
