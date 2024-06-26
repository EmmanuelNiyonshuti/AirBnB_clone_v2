#!/usr/bin/python3
"""
Starts a flask web application for AirBnB clone and
comprises a '/states_list' route function for displaying the states objs.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def display_states():
    """
    list all states objects in a format <state.id>: <B><state.name></B>
    """
    state_objs = storage.all(State)
    return render_template('7-states_list.html', states=state_objs)


@app.teardown_appcontext
def teardown_db(exception):
    """close the connection to the database"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
