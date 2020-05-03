# import dependencies
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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# precipiation page
# retreive the average prcp every day for the past 12 months and order by the date
@app.route("/api/v1.0/precipitation")
def precipiation():
    session = Session(engine)
    precipitation = session.query(Measurement.date, func.avg(Measurement.prcp)).\
        filter(Measurement.date > "2016-08-23").\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    
    # add all data into a list to be jsonified
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

    # make the format of data jsonifyable
    all_stations = list(np.ravel(station))
    return jsonify(all_stations)

# tobs page
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # find which station is the most active/has the most TOBs
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    # find TOB per day for the past 12 months for the most active station
    tob_12month = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station==most_active_station[0]).\
        filter(Measurement.date > '2016-08-18').\
        order_by(Measurement.date.desc()).all()
    session.close()

    # add all data into a list to be jsonified
    tobs_list = []
    for date, tobs in tob_12month:
        tob_12month_dict = {}
        tob_12month_dict["date"] = date
        tob_12month_dict["TOB"] = tobs
        tobs_list.append(tob_12month_dict)

    return jsonify(tobs_list)

# start date page
@app.route("/api/v1.0/<start>")
def start_normals(start):
    session = Session(engine)
    # finds the temp min, max, and average for each day after and including the date the user enters
    temp_normals_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    # add all data into a list to be jsonified
    start_list = []
    for tmin, tavg, tmax in temp_normals_start:
        start_list_dict = {}
        start_list_dict["TMIN"] = tmin
        start_list_dict["TAVG"] = tavg
        start_list_dict["TMAX"] = tmax
        start_list.append(start_list_dict)

    return jsonify(start_list)

# start and end date page
@app.route("/api/v1.0/<start>/<end>")
def startend_normals(start, end):
    session = Session(engine)
    # finds the temp min, max, and average for each day in between and including the dates the user enters
    temp_normals_startend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    # add all data into a list to be jsonified
    startend_list = []
    for tmin, tavg, tmax in temp_normals_startend:
        startend_list_dict = {}
        startend_list_dict["TMIN"] = tmin
        startend_list_dict["TAVG"] = tavg
        startend_list_dict["TMAX"] = tmax
        startend_list.append(startend_list_dict)

    return jsonify(startend_list)

# allows you to run the server from the command line with "python app.py"
if __name__ == '__main__':
    app.run(debug=True)