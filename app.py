import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("Running")
    return (
        f"API Routes:<br/>"
        f"Precipitation:/api/v1.0/precipitation<br/>"
        f"Stations:/api/v1.0/stations<br/>"
        f"Temperature Observations:/api/v1.0/tobs<br/>"
        f"Temperature Start:/api/v1.0/<start><br/>"
        f"Temperature Start to End:/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    sess = Session(engine)
    data = sess.query(Measurement.date, Measurement.prcp).filter(Measurement.date>(dt.date(2017,8,23) - dt.timedelta(days = 365))).order_by(Measurement.date).all()
    sess.close()

    all_data = []
    for date, prcp in data:
        dictionary = {}
        dictionary["date"] = date
        dictionary["prcp"] = prcp
        all_data.append(dictionary)

    return jsonify(all_data)
 
@app.route("/api/v1.0/stations")
def station():
    sess = Session(engine)
    active = (sess.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all())
    sess.close()

    stat = list(np.ravel(active))

    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tobs():
    sess = Session(engine)
    year_results = sess.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >(dt.date(2017,8,23) - dt.timedelta(days = 365))).order_by(Measurement.date).all()
    sess.close()

    result = list(np.ravel(year_results))

    return jsonify(result)

@app.route("/api/v1.0/<start>")
def start(start):
    sess = Session(engine)
    combined = sess.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    sess.close()

    store = []
    for min,max,avg in combined:
        diction = {}
        diction["TMIN"] = min
        diction["TMAX"] = max
        diction["TAVG"] = avg
        store.append(diction)

    return jsonify(store)

@app.route("/api/v1.0/<start>/<end>")
def starttoend(start, end):
    sess = Session(engine)
    combined_dates = sess.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    sess.close()

    end_result = []
    for min,max,avg in combined_dates:
        diction2 = {}
        diction2["TMIN"] = min
        diction2["TMAX"] = max
        diction2["TAVG"] = avg
        end_result.append(diction2)

    return jsonify(end_result)

if __name__ == "__main__":
    app.run(debug = True)
