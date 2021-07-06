import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    # Query precipitation for all dates in last 12 months
    months_twelve = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_twelve = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= months_twelve).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list 
    
    precip = []
    for prcp in precip_twelve:
        precip_dict = {}
        precip_dict["date"] = Date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of most active stations"""
    # Query all stations
    station_active = session.query(Measurement.station, func.count(Measurement.date)).\
        group_by(Measurement.station).order_by(func.count(Measurement.date).desc()).all()

    session.close()

    # Return a JSON list of stations from the dataset

    all_stations = list(np.ravel(station_active))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp_obs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the last 12 months of temperature observation data for most active station"""
    # Query all stations
    months_twelve = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    active_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281', Measurement.date >= months_twelve).all()

    session.close()

    # Return a JSON list of Tobs for most active stations from the last year
    
    return jsonify(active_temp)

@app.route("/api/v1.0/<start>")
def start_date():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the minimum temperature, the average temperature, and the max temperature
    T_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    session.close()
    
    # Return JSON list of the minimum temperature, the average temperature, and the max temperature
    start_d = []
    for min, max , avg in T_start
        start_dict = {}
        start_dict['min'] = min
        start_dict['max']= max
        start_dict['avg'] = avg
        start_d.append(start_dict)
    
    return jsonify(start_d)

@app.route("/api/v1.0/<start>/<end>")
def temp_range():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the minimum temperature, the average temperature, and the max temperature for date range
    T_range = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Return JSON list of the minimum temperature, the average temperature, and the max temperature
    range_d = []
    for min, max , avg in T_range
        range_dict = {}
        range_dict['min'] = min
        range_dict['max']= max
        range_dict['avg'] = avg
        start_d.append(range_dict)
    
    return jsonify(range_d)

if __name__ == '__main__':
    app.run(debug=True)
