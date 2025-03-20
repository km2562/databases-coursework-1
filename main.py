import sqlite3
conn = sqlite3.connect('flight_management')
print ("Database has been created")

conn.execute("DROP TABLE IF EXISTS flight")
conn.execute("DROP TABLE IF EXISTS pilot")
conn.execute("DROP TABLE IF EXISTS destination")

conn.execute("CREATE TABLE flight (flight_id INTEGER NOT NULL, departure_id INTEGER, destination_id INTEGER, departure_time DATETIME, duration_minutes INTEGER, arrival_time DATETIME, pilot_id INTEGER, status VARCHAR(15))")
conn.execute("CREATE TABLE pilot (pilot_id INTEGER NOT NULL, first_name VARCHAR(50), last_name VARCHAR(50), date_of_birth DATE, date_hired DATE)")
conn.execute("CREATE TABLE destination (location_id INTEGER NOT NULL, location_name VARCHAR(50), airport_code VARCHAR(3))")

print ("Tables created successfully")

# Now insert some data

conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (1, 'Joseph','Bloggs','1972-05-06','2015-06-17')");
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (2, 'Josephine','Doe','1986-12-08','2022-05-31')");

conn.execute("INSERT INTO destination (location_id, location_name, airport_code) VALUES (1, 'London Gatwick', 'LGW')");
conn.execute("INSERT INTO destination (location_id, location_name, airport_code) VALUES (2, 'London Luton', 'LTN')");
conn.execute("INSERT INTO destination (location_id, location_name, airport_code) VALUES (3, 'London Heathrow', 'LHR')");
conn.execute("INSERT INTO destination (location_id, location_name, airport_code) VALUES (4, 'Split', 'SPU')");
conn.execute("INSERT INTO destination (location_id, location_name, airport_code) VALUES (5, 'Corfu', 'CFU')");
conn.execute("INSERT INTO destination (location_id, location_name, airport_code) VALUES (6, 'Pula', 'PUY')");

conn.execute("INSERT INTO flight (flight_id, departure_id, destination_id, departure_time, duration_minutes, arrival_time, pilot_id, status) VALUES (1, 1, 3, '2025-05-10 07:10', '125', NULL, 2, 'Not departed')");

conn.commit()

print("Records created successfully")
print("Total number of rows created :", conn.total_changes)
print("\n");

# Show all the flight data

cursor = conn.execute("SELECT flight_id, source.location_name, dest.location_name, departure_time, duration_minutes, arrival_time, first_name, last_name, status \
   FROM flight, pilot, destination AS source, destination AS dest \
   WHERE flight.pilot_id = pilot.pilot_id and source.location_id = flight.departure_id AND dest.location_id = flight.destination_id")

for row in cursor:
   print("flight_id = ", row[0])
   print("departure = ", row[1])
   print("arrival = ", row[2])
   print("departure_time = ", row[3])
   print("duration_minutes = ", row[4])
   print("arrival_time = ", row[5])  
   print("pilot = ", row[6]+" "+row[7])
   print("status = ", row[8], "\n")


# Show menu
print("Menu options:")
print("1) View Flights")
print("2) Update a Flight")
print("3) View Pilots")
print("4) Update a Pilot")
print("5) View Destinations")
print("6) Update a Destinations")
print("7) Exit")

action = input("Enter your option \n")

if action == "1":
    print("1) selected")
elif action == "2":
    print("2) selected")
elif action == "3":
    print("3) selected")    
elif action == "4":
    print("4) selected")
elif action == "5":
    print("5) selected")
elif action == "6":
    print("6) selected")
elif action == "7":
    print("7) selected")
else:
    print("Input not recognised, try again")
