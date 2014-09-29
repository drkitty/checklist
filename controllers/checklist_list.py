from flask import render_template

from app import app


@app.route('/checklist')
def index():
    return render_template('checklist_list.html', rows=[
        (2, True, 'Buy birthday presents'),
        (5, False, 'Get more shoes'),
        (11, False, "Figure out where this term's classrooms are"),
    ])
