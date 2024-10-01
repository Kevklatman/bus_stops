#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from datetime import datetime, timedelta

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Passenger, BusStop, Favorite, Bus, Schedule

def create_passengers(num):
    passengers = []
    for _ in range(num):
        p = Passenger(
            name=fake.name(),
            email=fake.email(),
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
    used_numbers = set()
    for _ in range(num):
        while True:
            number = randint(100, 999)
            if number not in used_numbers:
                used_numbers.add(number)
                break
        b = Bus(
            number=str(number),  # Convert to string to match the Column type
            capacity=randint(20, 50)
        )
        buses.append(b)
    return buses

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
        schedules = create_schedules(100, buses, bus_stops)
        favorites = create_favorites(30, passengers, bus_stops)

        # Add all instances to session and commit
        db.session.add_all(passengers + bus_stops + buses + schedules + favorites)
        db.session.commit()

        print("Seed completed successfully!")