#!/usr/bin/env python3

from flask import make_response
from flask_restful import Resource, reqparse
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import Bus, Passenger, BusStop, Favorite, Schedule

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as e:
            return {'error': str(e)}, 400
        except ValueError as e:
            return {'error': str(e)}, 400
        except IntegrityError:
            db.session.rollback()
            return {'error': "Resource already exists"}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    return wrapper

class BaseResource(Resource):
    @handle_errors
    def get(self, id=None):
        if id:
            instance = self.model.query.get(id)
            return instance.to_dict() if instance else ({'error': f"{self.model.__name__} not found"}, 404)
        instances = self.model.query.all()
        return [instance.to_dict() for instance in instances]

class BusResource(BaseResource):
    model = Bus

class BusStopResource(BaseResource):
    model = BusStop

    @handle_errors
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        args = parser.parse_args()

        new_bus_stop = BusStop(**args)
        db.session.add(new_bus_stop)
        db.session.commit()
        return new_bus_stop.to_dict(), 201

class ScheduleResource(BaseResource):
    model = Schedule

    @handle_errors
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('bus_id', type=int, required=True)
        parser.add_argument('bus_stop_id', type=int, required=True)
        parser.add_argument('arrival_time', type=lambda x: datetime.fromisoformat(x), required=True)
        parser.add_argument('departure_time', type=lambda x: datetime.fromisoformat(x), required=True)
        args = parser.parse_args()

        new_schedule = Schedule(**args)
        db.session.add(new_schedule)
        db.session.commit()
        return new_schedule.to_dict(), 201

class PassengerResource(BaseResource):
    model = Passenger

    @handle_errors
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        new_passenger = Passenger(**args)
        db.session.add(new_passenger)
        db.session.commit()
        return new_passenger.to_dict(), 201

    @handle_errors
    def delete(self, id):
        passenger = Passenger.query.get(id)
        if not passenger:
            return {'error': "Passenger not found"}, 404
        db.session.delete(passenger)
        db.session.commit()
        return {'message': "Passenger deleted successfully"}, 200

class FavoriteResource(BaseResource):
    model = Favorite

    @handle_errors
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('passenger_id', type=int, required=True)
        parser.add_argument('bus_stop_id', type=int, required=True)
        args = parser.parse_args()

        passenger = Passenger.query.get(args['passenger_id'])
        bus_stop = BusStop.query.get(args['bus_stop_id'])

        if not passenger or not bus_stop:
            return {'error': "Passenger or Bus Stop not found"}, 404

        new_favorite = Favorite(**args)
        db.session.add(new_favorite)
        db.session.commit()
        return new_favorite.to_dict(), 201

    @handle_errors
    def delete(self, passenger_id, bus_stop_id):
        favorite = Favorite.query.filter_by(passenger_id=passenger_id, bus_stop_id=bus_stop_id).first()
        if not favorite:
            return {'error': "Favorite not found"}, 404
        db.session.delete(favorite)
        db.session.commit()
        return {'message': "Favorite deleted successfully"}, 200

class PassengerFavorites(Resource):
    @handle_errors
    def get(self, id):
        passenger = Passenger.query.get(id)
        if not passenger:
            return {'error': 'Passenger not found'}, 404

        response_data = {
            'id': passenger.id,
            'name': passenger.name,
            'email': passenger.email,
            'passenger_favorites': []
        }

        for favorite in passenger.favorites:
            bus_stop = favorite.bus_stop
            favorite_data = {
                'id': favorite.id,
                'bus_stop_id': favorite.bus_stop_id,
                'bus_stop_name': bus_stop.name,
                'bus_stop_location': bus_stop.location,
                'created_at': favorite.created_at.isoformat()
            }
            response_data['passenger_favorites'].append(favorite_data)

        return response_data, 200

api.add_resource(BusResource, '/buses', '/buses/<int:id>')
api.add_resource(BusStopResource, '/bus_stops', '/bus_stops/<int:id>')
api.add_resource(ScheduleResource, '/schedules', '/schedules/<int:id>')
api.add_resource(PassengerResource, '/passengers', '/passengers/<int:id>')
api.add_resource(FavoriteResource, '/favorites', '/favorites/<int:passenger_id>/<int:bus_stop_id>')
api.add_resource(PassengerFavorites, '/passenger_favorites/<int:id>')
#
if __name__ == '__main__':
    app.run(port=5555, debug=True)