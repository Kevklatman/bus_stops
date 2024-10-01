#models.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db
from sqlalchemy.ext.associationproxy import association_proxy

class Bus(db.Model, SerializerMixin):
    __tablename__ = "buses"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    schedules = db.relationship('Schedule', back_populates='bus', cascade='all, delete-orphan') 
    bus_stops = association_proxy('schedules', 'bus_stop')
    serialize_rules = ('-schedules.bus',)
    serialize_only = ('id', 'number', 'capacity')

    def __repr__(self):
        return f"<Bus {self.id}, {self.number}, {self.capacity}>"

class Passenger(db.Model, SerializerMixin):
    __tablename__ = "passengers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    password = db.Column(db.String)

    favorites = db.relationship('Favorite', back_populates="passenger", cascade='all, delete-orphan')
    bus_stops = association_proxy('favorites', 'bus_stop')

    serialize_rules = ('-favorites.passenger',)
    serialize_only = ('id', 'name', 'email')
    
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("No name provided")
        return name

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email is required")
        if '@' not in email:
            raise ValueError("Must provide a valid email address")
        return email

    def __repr__(self):
        return f"<Passenger {self.name}, {self.email}>"

class BusStop(db.Model, SerializerMixin):
    __tablename__ = "bus_stops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    comments = db.Column(db.String) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    favorites = db.relationship('Favorite', back_populates='bus_stop')
    passengers = association_proxy('favorites', 'passenger')
    schedules = db.relationship('Schedule', back_populates='bus_stop')
    bus_stops = association_proxy('schedules', 'bus_stop')

    serialize_rules = ('-favorites.bus_stop', '-schedules.bus_stop')
    serialize_only = ('id', 'name', 'location', 'comments')  

    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise AssertionError("No name provided")
        if BusStop.query.filter(BusStop.name == name).first():
            raise AssertionError("Bus stop name is already in use")
        if len(name) < 3 or len(name) > 90:
            raise AssertionError("Bus stop name must be between 3 and 90 characters")
        return name

    def __repr__(self):
        return f"<BusStop {self.name}, {self.location}>"



class Favorite(db.Model, SerializerMixin):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.id'))
    bus_stop_id = db.Column(db.Integer, db.ForeignKey('bus_stops.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())


    passenger = db.relationship('Passenger', back_populates='favorites')
    bus_stop = db.relationship('BusStop', back_populates='favorites')

    serialize_rules = ('-passenger.favorites', '-bus_stop.favorites')
    serialize_only = ('id','passenger_id', 'bus_stop_id', 'created_at')
    def __repr__(self):
        return f"<Favorite {self.id}, {self.passenger_id}, {self.created_at}>"

class Schedule(db.Model, SerializerMixin):
    __tablename__ = "schedules"

    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    bus_stop_id = db.Column(db.Integer, db.ForeignKey('bus_stops.id'))
    arrival_time = db.Column(db.DateTime, nullable = False)
    departure_time = db.Column(db.DateTime, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    bus = db.relationship('Bus', back_populates='schedules')
    bus_stop = db.relationship('BusStop', back_populates='schedules')

    serialize_rules = ('-bus.schedules', '-bus_stop.schedules')
    serialize_only = ('id', 'bus_id', 'bus_stop_id', 'arrival_time', 'departure_time', 'created_at')


    @validates("arrival_time", "departure_time")
    def validate_times(self, key, time):
        if key == "arrival_time" and self.departure_time and time > self.departure_time:
            raise AssertionError("Arrival time must be before departure time")
        elif key == "departure_time" and self.arrival_time and time < self.arrival_time:
            raise AssertionError("Departure time must be after arrival time")
        return time 

    def __repr__(self):
        return f"<Schedule Bus NO: {self.bus.number}>"