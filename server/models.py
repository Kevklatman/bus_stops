from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from config import db
#blah blah blah
# Models go here!
class Passenger(db.Model, SerializerMixin):
    __tablename__ = 'passengers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    favorites = relationship('Favorite', back_populates='passenger')
    comments = relationship('Comment', back_populates='passenger')

class BusStop(db.Model, SerializerMixin):
    __tablename__ = 'bus_stops'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    favorites = relationship('Favorite', back_populates='bus_stop')
    comments = relationship('Comment', back_populates='bus_stop')
    schedules = relationship('Schedule', back_populates='bus_stop')

class Favorite(db.Model, SerializerMixin):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True)
    passenger_id = Column(Integer, ForeignKey('passengers.id'))
    bus_stop_id = Column(Integer, ForeignKey('bus_stops.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    passenger = relationship('Passenger', back_populates='favorites')
    bus_stop = relationship('BusStop', back_populates='favorites')

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    passenger_id = Column(Integer, ForeignKey('passengers.id'))
    bus_stop_id = Column(Integer, ForeignKey('bus_stops.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    passenger = relationship('Passenger', back_populates='comments')
    bus_stop = relationship('BusStop', back_populates='comments')

class Bus(db.Model, SerializerMixin):
    __tablename__ = 'busses'

    id = Column(Integer, primary_key=True)
    number = Column(String)
    capacity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    schedules = relationship('Schedule', back_populates='bus')
    routes = relationship('Route', back_populates='bus')

class Schedule(db.Model, SerializerMixin):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    arrival_time = Column(DateTime)
    departure_time = Column(DateTime)
    bus_id = Column(Integer, ForeignKey('busses.id'))
    bus_stop_id = Column(Integer, ForeignKey('bus_stops.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    bus = relationship('Bus', back_populates='schedules')
    bus_stop = relationship('BusStop', back_populates='schedules')

class Route(db.Model, SerializerMixin):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    bus_id = Column(Integer, ForeignKey('busses.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    bus = relationship('Bus', back_populates='routes')