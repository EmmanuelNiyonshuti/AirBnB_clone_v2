#!/usr/bin/python3
"""
Starts a Flask web application for AirBnB clone and
comprises a '/cities_by_states' for rendering the HTML page
cities associated with a particular state.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_cities(id=None):
    """
    List all states or cities within a particular state.
    """
    states = storage.all(State)
    state_city = None
    if id:
        for obj in states.values():
            if obj.id == id:
                state_city = obj
                break
        return render_template('9-states.html', state=state_city)
    else:
        return render_template('9-states.html', states=states.values())


@app.teardown_appcontext
def teardown_db(exception):
    """
    Close the connection to the database.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
