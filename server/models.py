from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class Bus(db.Model, SerializerMixin):
    __tablename__ = "buses"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    schedules = db.relationship('Schedule', back_populates='bus', )#cascade='all, delete-orphan' <I don't think we'll need this line commenting out for now>

    serialize_rules = ('-schedules.bus',)
    serialize_only = ('id', 'number', 'capacity')

    def __repr__(self):
        return f"<Bus {self.id}, {self.number}, {self.capacity}>"

class Passenger(db.Model, SerializerMixin):
    __tablename__ = "passengers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    favorites = db.relationship('Favorite', back_populates="passenger", cascade='all, delete-orphan')

    serialize_rules = ('-favorites.passenger',)
    serialize_only = ('id', 'name', 'email')
    
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise AssertionError("No name provided")
        return name

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Must provide a valid email address")
        return address

    def __repr__(self):
        return f"<Passenger {self.name}, {self.email}>"

class BusStop(db.Model, SerializerMixin):
    __tablename__ = "bus_stops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    favorites = db.relationship('Favorite', back_populates='bus_stop')
    schedules = db.relationship('Schedule', back_populates='bus_stop')

    serialize_rules = ('-favorites.bus_stop', '-schedules.bus_stop')
    serialize_only = ('id', 'name', 'location')

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

    def __repr__(self):
        return f"<Favorite {self.id}, {self.passenger_id}, {self.created_at}>"

class Schedule(db.Model, SerializerMixin):
    __tablename__ = "schedules"

    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))
    bus_stop_id = db.Column(db.Integer, db.ForeignKey('bus_stops.id'))
    arrival_time = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    bus = db.relationship('Bus', back_populates='schedules')
    bus_stop = db.relationship('BusStop', back_populates='schedules')

    serialize_rules = ('-bus.schedules', '-bus_stop.schedules')
    serialize_only = ('id', 'bus_id', 'bus_stop_id', 'arrival_time', 'departure_time', 'created_at')

    __table_args__ = (db.UniqueConstraint("bus_id", "arrival_time", "bus_stop_id"),)

    @validates("arrival_time", "departure_time")
    def validate_times(self, key, time):
        if key == "arrival_time" and self.departure_time and time > self.departure_time:
            raise AssertionError("Arrival time must be before departure time")
        elif key == "departure_time" and self.arrival_time and time < self.arrival_time:
            raise AssertionError("Departure time must be after arrival time")
        return time 

    def __repr__(self):
        return f"<Schedule Bus NO: {self.bus.number}>"