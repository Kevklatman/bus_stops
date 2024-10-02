## info doc for API Resources in app.py

### Buses
- Endpoint: `/buses`
- Methods:
  - GET: Retrieve all buses
  - POST: Create a new bus
- Endpoint: `/buses/<int:id>`
- Methods:
  - GET: Retrieve a specific bus by ID
  - PATCH: Update a specific bus by ID
  - DELETE: Delete a specific bus by ID

### Bus Stops
- Endpoint: `/bus_stops`
- Methods:
  - GET: Retrieve all bus stops
  - POST: Create a new bus stop
- Endpoint: `/bus_stops/<int:id>`
- Methods:
  - GET: Retrieve a specific bus stop by ID
  - PATCH: Update a specific bus stop by ID
  - DELETE: Delete a specific bus stop by ID

### Schedules
- Endpoint: `/schedules`
- Methods:
  - GET: Retrieve all schedules
  - POST: Create a new schedule
- Endpoint: `/schedules/<int:id>`
- Methods:
  - GET: Retrieve a specific schedule by ID

### Passengers
- Endpoint: `/passengers`
- Methods:
  - GET: Retrieve all passengers
  - POST: Create a new passenger
- Endpoint: `/passengers/<int:id>`
- Methods:
  - GET: Retrieve a specific passenger by ID
  - PATCH: Update a specific passenger by ID
  - DELETE: Delete a specific passenger by ID

### Favorites
- Endpoint: `/favorites`
- Methods:
  - GET: Retrieve all favorites
  - POST: Create a new favorite
- Endpoint: `/favorites/<int:id>`
- Methods:
  - GET: Retrieve a specific favorite by ID
  - DELETE: Delete a specific favorite by ID
- Endpoint: `/favorites/<int:passenger_id>/<int:bus_stop_id>`
- Methods:
  - DELETE: Delete a specific favorite by passenger ID and bus stop ID

### Passenger Favorites
- Endpoint: `/passenger_favorites/<int:id>`
- Methods:
  - GET: Retrieve favorites for a specific passenger by ID

### Bus Stops for Bus
- Endpoint: `/buses/<int:bus_id>/bus_stops`
- Methods:
  - GET: Retrieve all bus stops for a specific bus by ID

### Schedules for Bus Stop
- Endpoint: `/bus_stops/<int:bus_stop_id>/schedules`
- Methods:
  - GET: Retrieve all schedules for a specific bus stop by ID