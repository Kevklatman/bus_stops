#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response
from flask_restful import Resource
from datetime import datetime
from sqlalchemy.exc import IntegrityError

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
    
class BusSchedulesList(Resource):
    def get(self):
        schedules = Schedule.query.all()
        return [schedule.to_dict() for schedule in schedules]
    
class PassengerList(Resource):
    def get(self):
        passengers = Passenger.query.all()
        return [passenger.to_dict() for passenger in passengers]
    
class PassengerFavorite(Resource):
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

    def post(self):
        data = request.get_json()
        try:
            passenger_id = data['passenger_id']
            bus_stop_id = data['bus_stop_id']
            created_at = datetime.fromisoformat(data['created_at'])

            # passenger exists?
            passenger = Passenger.query.get(passenger_id)
            if not passenger:
                return make_response({"errors": ["Passenger not found"]}, 404)

            # stop exists?
            bus_stop = BusStop.query.get(bus_stop_id)
            if not bus_stop:
                return make_response({"errors": ["Bus stop not found"]}, 404)

            # is duplicate?
            existing_favorite = Favorite.query.filter_by(passenger_id=passenger_id, bus_stop_id=bus_stop_id).first()
            if existing_favorite:
                return make_response({"errors": ["Favorite already exists"]}, 409)

            new_favorite_stop = Favorite(
                passenger_id=passenger_id,
                bus_stop_id=bus_stop_id,
                created_at=created_at
            )
            db.session.add(new_favorite_stop)
            db.session.commit()
            response_data = new_favorite_stop.to_dict()
            return make_response(response_data, 201)

        except KeyError as e:
            return make_response({"errors": [f"Missing field: {str(e)}"]}, 400)
        except ValueError as e:
            return make_response({"errors": [str(e)]}, 400)
        except AssertionError as e:
            return make_response({"errors": [str(e)]}, 400)
        except Exception as e:
            db.session.rollback()
            return make_response({"errors": [str(e)]}, 500)
        
    def delete(self, passenger_id, bus_stop_id):
        try:
            # passenger exists
            passenger = Passenger.query.get(passenger_id)
            if not passenger:
                return make_response({"errors": ["Passenger not found"]}, 404)

            # stop exists?
            bus_stop = BusStop.query.get(bus_stop_id)
            if not bus_stop:
                return make_response({"errors": ["Bus stop not found"]}, 404)

            # fave exists?
            favorite = Favorite.query.filter_by(passenger_id=passenger_id, bus_stop_id=bus_stop_id).first()
            if not favorite:
                return make_response({"errors": ["Favorite not found"]}, 404)

            db.session.delete(favorite)
            db.session.commit()
            return make_response({"message": "Favorite deleted successfully"}, 200)

        except Exception as e:
            db.session.rollback()
            return make_response({"errors": [str(e)]}, 500)
    



    


api.add_resource(BusStopList, '/bus_stops')
api.add_resource(BusList, '/buses')
api.add_resource(BusSchedulesList, '/schedules')
api.add_resource(PassengerList, '/passengers')
api.add_resource(PassengerFavorite, '/favorites', '/favorites/<int:id>', '/favorites/<int:passenger_id>/<int:bus_stop_id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

#