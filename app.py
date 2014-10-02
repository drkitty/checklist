from flask import Flask, render_template

import settings.python as settings


app = Flask(__name__)
for name, value in settings.app_config.items():
    setattr(app, name, value)
