#!/usr/bin/python3
"""
Starts a flask web application for AirBnB clone.
"""
import os
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
    
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """close the connection to the database"""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def states_cities():
    """list all cities with in a particular state"""
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':

        states_objs = storage.all(State).values()
        return render_template('8-cities_by_states.html', states=states_objs)
    else:
        states_objs = storage.all(State).values()
        return render_template('8-cities_by_states.html', states=states_objs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
