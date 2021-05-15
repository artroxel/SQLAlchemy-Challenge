from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("Running")
    return (
        f"API Routes"
        f"Precipitation:/api/v1.0/precipitation"
        f"Stations: /api/v1.0/stations"
        f"Temperature Observations: /api/v1.0/tobs"
    )



if __name__ == "__main__":
    app.run(debug = True)