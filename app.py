import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

# home page
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to my Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# precipiation page
@app.route("/api/v1.0/precipitation")
def precipiation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precipitation_list = []
    for date, prcp in precipitation:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)

# station page
# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station = session.query(Station.station).all()
    session.close()

    all_stations = list(np.ravel(station))
    return jsonify(all_stations)

# tobs page
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    station = session.query(Measurement.date, Measurement.tobs).\
        filter().all()
    session.close()



# # start date page
# @app.route("/api/v1.0/<start>")
# def start():


# # start and end date page
# @app.route("/api/v1.0/<start>/<end>")
# def startend():


if __name__ == '__main__':
    app.run(debug=True)