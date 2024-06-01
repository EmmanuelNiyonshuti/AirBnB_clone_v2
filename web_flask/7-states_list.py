#!/usr/bin/python3
"""Starts a flask web application"""
import os
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def states():
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        states_objs = storage.all(State).values()
        return render_template('7-states_list.html', states= states_objs)
    else:
        states_objs = storage.all(State).values()
        return render_template('7-states_list.html', states= states_objs)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)