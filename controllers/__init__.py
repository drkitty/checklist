from flask import Flask


app = Flask('controllers')


@app.route('/')
def index():
    return "Hello, world!"
