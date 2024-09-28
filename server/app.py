#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import *

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class BusStopList(Resource):
    def get(self):
        bus_stops = BusStop.query.all()
        return [bus_stop.to_dict() for bus_stop in bus_stops]
    
class BusList(Resource):
    def get(self):
        buses = Bus.query.all()
        return [bus.to_dict() for bus in buses]
    
class PassengerHandling(Resource):
    def get(self):
        passengers = Passenger.query.all()
        return [passenger.to_dict() for passenger in passengers]
    

    


api.add_resource(BusStopList, '/bus_stops')
api.add_resource(BusList, '/buses')
api.add_resource(PassengerHandling, '/passengers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

#