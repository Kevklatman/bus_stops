from flask import make_response, jsonify, request, current_app
from flask_restful import Resource
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS

from config import app, db, api
from models import Bus, Passenger, BusStop, Favorite, Schedule

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Passenger.query.get(int(user_id))

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class BusResource(Resource):
    def get(self, id=None):
        if id:
            bus = Bus.query.get(id)
            if bus:
                return make_response(jsonify(bus.to_dict()), 200)
            return make_response(jsonify({'error': "Bus not found"}), 404)
        buses = Bus.query.all()
        return make_response(jsonify([bus.to_dict() for bus in buses]), 200)

    def post(self):
        data = request.get_json()
        new_bus = Bus(**data)
        db.session.add(new_bus)
        db.session.commit()
        return make_response(jsonify(new_bus.to_dict()), 201)

    def patch(self, id):
        bus = Bus.query.get(id)
        if not bus:
            return make_response(jsonify({'error': "Bus not found"}), 404)
        data = request.get_json()
        for key, value in data.items():
            setattr(bus, key, value)
        db.session.commit()
        return make_response(jsonify(bus.to_dict()), 200)

    def delete(self, id):
        bus = Bus.query.get(id)
        if not bus:
            return make_response(jsonify({'error': "Bus not found"}), 404)
        db.session.delete(bus)
        db.session.commit()
        return make_response(jsonify({'message': "Bus deleted successfully"}), 200)

class BusStopResource(Resource):
    def get(self, id=None):
        if id:
            bus_stop = BusStop.query.get(id)
            if bus_stop:
                return make_response(jsonify(bus_stop.to_dict()), 200)
            return make_response(jsonify({'error': "Bus Stop not found"}), 404)
        bus_stops = BusStop.query.all()
        return make_response(jsonify([bus_stop.to_dict() for bus_stop in bus_stops]), 200)

    def post(self):
        data = request.get_json()
        new_bus_stop = BusStop(**data)
        db.session.add(new_bus_stop)
        db.session.commit()
        return make_response(jsonify(new_bus_stop.to_dict()), 201)

    def patch(self, id):
        bus_stop = BusStop.query.get(id)
        if not bus_stop:
            return make_response(jsonify({'error': "Bus Stop not found"}), 404)

        data = request.get_json()
        for key, value in data.items():
            setattr(bus_stop, key, value)

        try:
            db.session.commit()
            return make_response(jsonify(bus_stop.to_dict()), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 400)

    def delete(self, id):
        bus_stop = BusStop.query.get(id)
        if not bus_stop:
            return make_response(jsonify({'error': "Bus Stop not found"}), 404)
        db.session.delete(bus_stop)
        db.session.commit()
        return make_response(jsonify({'message': "Bus Stop deleted successfully"}), 200)

class ScheduleResource(Resource):
    def get(self, id=None):
        if id:
            schedule = Schedule.query.get(id)
            if schedule:
                return make_response(jsonify(schedule.to_dict()), 200)
            return make_response(jsonify({'error': "Schedule not found"}), 404)
        schedules = Schedule.query.all()
        return make_response(jsonify([schedule.to_dict() for schedule in schedules]), 200)

    def post(self):
        data = request.get_json()
        data['arrival_time'] = datetime.fromisoformat(data['arrival_time'])
        data['departure_time'] = datetime.fromisoformat(data['departure_time'])
        new_schedule = Schedule(**data)
        db.session.add(new_schedule)
        db.session.commit()
        return make_response(jsonify(new_schedule.to_dict()), 201)

class PassengerResource(Resource):
    def get(self, id=None):
        if id:
            passenger = Passenger.query.get(id)
            if passenger:
                return make_response(jsonify(passenger.to_dict()), 200)
            return make_response(jsonify({'error': "Passenger not found"}), 404)
        passengers = Passenger.query.all()
        return make_response(jsonify([passenger.to_dict() for passenger in passengers]), 200)

    def post(self):
        data = request.get_json()
        new_passenger = Passenger(
            name=data['name'],
            email=data['email'],
        )
        #password_hash= data.get('password') will enable the @password_hash.setter thus running the encryption that was written in models.py
        #Set the password using the setter method
        new_passenger.password_hash = data['password'] 
        try:
            db.session.add(new_passenger)
            db.session.commit()
            return make_response(jsonify(new_passenger.to_dict()), 201)
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig)
            if "UNIQUE constraint failed: passengers.email" in error_message:
                return make_response(jsonify({'error': "Passenger with this email already exists"}), 409)
            else:
                return make_response(jsonify({'error': "An error occurred while creating the passenger"}), 500)

    def patch(self, id):
        passenger = Passenger.query.get(id)
        if not passenger:
            return make_response(jsonify({'error': "Passenger not found"}), 404)
        
        data = request.get_json()
        for key, value in data.items():
            setattr(passenger, key, value)
        
        try:
            db.session.commit()
            return make_response(jsonify(passenger.to_dict()), 200)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': "Email already in use"}), 409)
    def delete(self, id):
        try:
            passenger = Passenger.query.get(id)
            if not passenger:
                current_app.logger.info(f"Attempted to delete non-existent passenger with id {id}")
                return make_response(jsonify({'error': "Passenger not found"}), 404)
            
            current_app.logger.info(f"Deleting passenger with id {id}")
            db.session.delete(passenger)
            db.session.commit()
            current_app.logger.info(f"Successfully deleted passenger with id {id}")
            return make_response(jsonify({'message': "Passenger deleted successfully"}), 200)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting passenger with id {id}: {str(e)}")
            return make_response(jsonify({'error': "An error occurred while deleting the passenger"}), 500)
        
        except Exception as e:
            current_app.logger.error(f"Unexpected error deleting passenger with id {id}: {str(e)}")
            return make_response(jsonify({'error': "An unexpected error occurred"}), 500)
class FavoriteResource(Resource):
    def get(self, id=None):
        if id:
            favorite = Favorite.query.get(id)
            if favorite:
                return make_response(jsonify(favorite.to_dict()), 200)
            return make_response(jsonify({'error': "Favorite not found"}), 404)
        favorites = Favorite.query.all()
        return make_response(jsonify([favorite.to_dict() for favorite in favorites]), 200)

    @login_required
    def post(self):
        try:
            data = request.get_json()
            passenger_id = current_user.id
            bus_stop_id = data.get('bus_stop_id')

            current_app.logger.info(f"Adding favorite for passenger {passenger_id}, bus stop {bus_stop_id}")

            if not bus_stop_id:
                return make_response(jsonify({'error': "Bus Stop ID is required"}), 400)

            bus_stop = BusStop.query.get(bus_stop_id)

            if not bus_stop:
                return make_response(jsonify({'error': "Bus Stop not found"}), 404)

            existing_favorite = Favorite.query.filter_by(passenger_id=passenger_id, bus_stop_id=bus_stop_id).first()
            if existing_favorite:
                current_app.logger.info(f"Favorite already exists for passenger {passenger_id}, bus stop {bus_stop_id}")
                return make_response(jsonify({'message': "Favorite already exists", 'favorite': existing_favorite.to_dict()}), 200)

            new_favorite = Favorite(passenger_id=passenger_id, bus_stop_id=bus_stop_id)
            db.session.add(new_favorite)
            try:
                db.session.commit()
                current_app.logger.info(f"New favorite added for passenger {passenger_id}, bus stop {bus_stop_id}")
                return make_response(jsonify({'message': "Favorite added successfully", 'favorite': new_favorite.to_dict()}), 201)
            except IntegrityError:
                db.session.rollback()
                current_app.logger.warning(f"IntegrityError: Favorite already exists for passenger {passenger_id}, bus stop {bus_stop_id}")
                return make_response(jsonify({'message': "Favorite already exists"}), 200)
        except Exception as e:
            current_app.logger.error(f"Error in FavoriteResource: {str(e)}")
            return make_response(jsonify({'error': 'Internal server error'}), 500)

    def delete(self, id):
        favorite = Favorite.query.get(id)
        if not favorite:
            return make_response(jsonify({'error': "Favorite not found"}), 404)
        db.session.delete(favorite)
        db.session.commit()
        return make_response(jsonify({'message': "Favorite deleted successfully"}), 200)

class PassengerFavorites(Resource):
    def get(self, id):
        passenger = Passenger.query.get(id)
        if not passenger:
            return make_response(jsonify({'error': 'Passenger not found'}), 404)

        response_data = {
            'id': passenger.id,
            'name': passenger.name,
            'email': passenger.email,
            'passenger_favorites': []
        }

        for bus_stop in passenger.bus_stops:
            favorite_data = {
                'bus_stop_id': bus_stop.id,
                'bus_stop_name': bus_stop.name,
                'bus_stop_location': bus_stop.location
            }
            response_data['passenger_favorites'].append(favorite_data)

        return make_response(jsonify(response_data), 200)
    
class BusStopsForBus(Resource):
    def get(self, bus_id):
        bus = Bus.query.get(bus_id)
        if not bus:
            return make_response(jsonify({'error': 'Bus not found'}), 404)

        bus_stops = BusStop.query.join(Schedule).filter(Schedule.bus_id == bus_id).all()

        response_data = {
            'bus_id': bus.id,
            'bus_number': bus.number,
            'bus_stops': [bus_stop.to_dict() for bus_stop in bus_stops]
        }

        return make_response(jsonify(response_data), 200)
        
class SchedulesForBusStop(Resource):
    def get(self, bus_stop_id):
        bus_stop = BusStop.query.get(bus_stop_id)
        if not bus_stop:
            return make_response(jsonify({'error': 'Bus stop not found'}), 404)

        schedules = Schedule.query.filter(Schedule.bus_stop_id == bus_stop_id).all()

        response_data = {
            'bus_stop_id': bus_stop.id,
            'bus_stop_name': bus_stop.name,
            'schedules': [schedule.to_dict() for schedule in schedules]
        }

        return make_response(jsonify(response_data), 200)
    
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return make_response(jsonify({'error': 'Email and password required'}), 400)

        passenger = Passenger.query.filter_by(email=email).first()

        if passenger and passenger.authenticate(password):
            login_user(passenger)  
            return make_response(jsonify({'message': 'Login successful', 'user': passenger.to_dict()}), 200)

        return make_response(jsonify({'error': 'Invalid email or password'}), 401)
    
class LogoutResource(Resource):
    @login_required
    def post(self):
        logout_user()
        return make_response(jsonify({'message': 'Logged out successfully'}), 200)

class CheckSessionResource(Resource):
    def get(self):
        try:
            if current_user.is_authenticated:
                return make_response({
                    'id': current_user.id,
                    'email': current_user.email,
                }, 200)
            return make_response({'error': 'User not authenticated'}, 401)
        except Exception as e:
            current_app.logger.error(f"Error in CheckSessionResource: {str(e)}")
            return make_response({'error': 'Internal server error'}, 500)
        
@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

api.add_resource(BusResource, '/buses', '/buses/<int:id>')
api.add_resource(BusStopResource, '/bus_stops', '/bus_stops/<int:id>')
api.add_resource(ScheduleResource, '/schedules', '/schedules/<int:id>')
api.add_resource(PassengerResource, '/passengers', '/passengers/<int:id>')
api.add_resource(FavoriteResource, '/favorites', '/favorites/<int:id>')
api.add_resource(PassengerFavorites, '/passenger_favorites/<int:id>')
api.add_resource(BusStopsForBus, '/buses/<int:bus_id>/bus_stops')
api.add_resource(SchedulesForBusStop, '/bus_stops/<int:bus_stop_id>/schedules')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(CheckSessionResource, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)