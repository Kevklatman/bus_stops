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
    
class PassengerList(Resource):
    def get(self):
        passengers = Passenger.query.all()
        return [passenger.to_dict() for passenger in passengers]
    
class PassengerFavorites(Resource):
    def get(self, id):
        passenger = Passenger.query.get(id)
        if passenger:
            passenger_data = passenger.to_dict()

            response_data = {
                'id': passenger_data['id'],
                'name': passenger_data['name'],
                'email': passenger_data['email'],
                'passenger_favorites': []
            }
            
            for favorite in passenger.favorites:
                bus_stop = favorite.bus_stop
                bus_stop_data = bus_stop.to_dict()
                
                favorite_data = {
                    'id': favorite.id,
                    'bus_stop_id': favorite.bus_stop_id,
                    'bus_stop_name': bus_stop_data['name'],
                    'bus_stop_location': bus_stop_data['location'],
                    'created_at': favorite.created_at.isoformat()
                }
                
                response_data['passenger_favorites'].append(favorite_data)
            
            return response_data, 200
        else:
            return {'error': 'Passenger not found'}, 404
    

    


api.add_resource(BusStopList, '/bus_stops')
api.add_resource(BusList, '/buses')
api.add_resource(PassengerList, '/passengers')
api.add_resource(PassengerFavorites, '/favorites/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

#