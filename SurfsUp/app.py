# Import the dependencies.
import numpy as np
import datetime as dt

from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement`
Measurement = Base.classes.measurement

# the station class to a variable called `Station`
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Landing page definition and list of available routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Surfs Up API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>")

# Precipitation route to query the precipitation data for the last year with the date as the key value of the dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for Precipitation Data")
    date = "2016-08-23"
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date).all()
    precipitation_data = []
    for date, prcp in query:
        data_dictionary = {}
        data_dictionary[date] = prcp
        precipitation_data.append(data_dictionary)
    return jsonify(precipitation_data)

# Stations route to query the available information of all weather stations
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for Stations Data")
    query = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    station_data = []
    for station_id, name, lat, lon, elevation in query:
        data_dictionary = {}
        data_dictionary["Station ID"] = station_id
        data_dictionary["Name"] = name
        data_dictionary["Latitude"] = lat
        data_dictionary["Longitude"] = lon
        data_dictionary["Elevation"] = elevation
        station_data.append(data_dictionary)
    return jsonify(station_data)

# Temperature route to query the temperature data of the most active weather station
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for Temperatures of the most active Station")
    date = "2016-08-23"
    most_active_station = "USC00519281"
    query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= date).filter(Measurement.station == most_active_station).all()
    temp_data = []
    for date, temp in query:
        data_dictionary = {}
        data_dictionary["Station ID"] = most_active_station
        data_dictionary["Date"] = date
        data_dictionary["Temperature"] = temp
        temp_data.append(data_dictionary)
    return jsonify(temp_data)

# Dynamic route to query the min, max, and average temperatures calculated from the given start date to the end of the dataset
@app.route("/api/v1.0/<start_date>")
def temp_basic_summary(start_date):
    print(f"Server received request for Temperatures information from {start_date} ")
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    temp_summary = []
    for min_temp, avg_temp, max_temp in query:
        data_dictionary = {}
        data_dictionary["Minimum Temperature"] = min_temp
        data_dictionary["Average Temperature"] = avg_temp
        data_dictionary["Maximum Temperature"] = max_temp
        temp_summary.append(data_dictionary)
    return jsonify(temp_summary)

# Dynamic route to query the min, max, and average temperatures calculated from the given start date to the given end date
@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_advanced_summary(start_date, end_date):
    print(f"Server received request for Temperatures information from {start_date} to {end_date}")
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    temp_summary = []
    for min_temp, avg_temp, max_temp in query:
        data_dictionary = {}
        data_dictionary["Minimum Temperature"] = min_temp
        data_dictionary["Average Temperature"] = avg_temp
        data_dictionary["Maximum Temperature"] = max_temp
        temp_summary.append(data_dictionary)
    return jsonify(temp_summary)

if __name__ == "__main__":
    app.run(debug=True)