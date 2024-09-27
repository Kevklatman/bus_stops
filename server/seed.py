#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from datetime import datetime, timedelta

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Passenger, BusStop, Favorite, Comment, Bus, Schedule, Route

def create_passengers(num):
    passengers = []
    for _ in range(num):
        p = Passenger(
            name=fake.name(),
            email=fake.email()
        )
        passengers.append(p)
    return passengers

def create_bus_stops(num):
    bus_stops = []
    for _ in range(num):
        bs = BusStop(
            name=fake.street_name() + " Stop",
            location=fake.address()
        )
        bus_stops.append(bs)
    return bus_stops

def create_buses(num):
    buses = []
    for _ in range(num):
        b = Bus(
            number=fake.license_plate(),
            capacity=randint(20, 50)
        )
        buses.append(b)
    return buses

def create_routes(num, buses):
    routes = []
    for _ in range(num):
        r = Route(
            name=fake.city() + " Route",
            description=fake.paragraph(),
            bus=rc(buses)
        )
        routes.append(r)
    return routes

def create_schedules(num, buses, bus_stops):
    schedules = []
    for _ in range(num):
        arrival_time = fake.date_time_this_year()
        s = Schedule(
            arrival_time=arrival_time,
            departure_time=arrival_time + timedelta(minutes=randint(5, 30)),
            bus=rc(buses),
            bus_stop=rc(bus_stops)
        )
        schedules.append(s)
    return schedules

def create_favorites(num, passengers, bus_stops):
    favorites = []
    for _ in range(num):
        f = Favorite(
            passenger=rc(passengers),
            bus_stop=rc(bus_stops)
        )
        favorites.append(f)
    return favorites

def create_comments(num, passengers, bus_stops):
    comments = []
    for _ in range(num):
        c = Comment(
            content=fake.paragraph(),
            passenger=rc(passengers),
            bus_stop=rc(bus_stops)
        )
        comments.append(c)
    return comments

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create instances
        passengers = create_passengers(50)
        bus_stops = create_bus_stops(20)
        buses = create_buses(10)
        routes = create_routes(5, buses)
        schedules = create_schedules(100, buses, bus_stops)
        favorites = create_favorites(30, passengers, bus_stops)
        comments = create_comments(40, passengers, bus_stops)

        # Add all instances to session and commit
        db.session.add_all(passengers + bus_stops + buses + routes + schedules + favorites + comments)
        db.session.commit()

        print("Seed completed successfully!")