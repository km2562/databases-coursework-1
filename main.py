import sqlite3
conn = sqlite3.connect('flight_management')
print ("Database has been created")

conn.execute("DROP TABLE IF EXISTS flight")
conn.execute("DROP TABLE IF EXISTS pilot")
conn.execute("DROP TABLE IF EXISTS airport")
conn.execute("DROP TABLE IF EXISTS route")

conn.execute("CREATE TABLE flight (flight_id INTEGER NOT NULL, route_id INTEGER, departure_time DATETIME, arrival_time DATETIME, pilot_id INTEGER, status VARCHAR(15))")
conn.execute("CREATE TABLE pilot (pilot_id INTEGER NOT NULL, first_name VARCHAR(50), last_name VARCHAR(50), date_of_birth DATE, date_hired DATE)")
conn.execute("CREATE TABLE route (route_id INTEGER NOT NULL, departure_airport_id INTEGER, arrival_airport_id INTEGER, duration_minutes INTEGER)")
conn.execute("CREATE TABLE airport (airport_id INTEGER NOT NULL, airport_name VARCHAR(50), airport_code VARCHAR(3), country VARCHAR(50))")

print ("Tables created successfully")

# Now insert some data

conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (1, 'Joseph','Bloggs','1972-05-06','2015-06-17')");
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (2, 'Josephine','Doe','1986-12-08','2022-05-31')");

conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (1, 'London Gatwick', 'LGW', 'UK')");
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (2, 'London Luton', 'LTN', 'UK')");
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (3, 'London Heathrow', 'LHR', 'UK')");
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (4, 'Split', 'SPU', 'Croatia')");
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (5, 'Corfu', 'CFU', 'Greece')");
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (6, 'Pula', 'PUY', 'Croatia')");

conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) \
   SELECT ROW_NUMBER() OVER (ORDER BY d1.airport_id), d1.airport_id, d2.airport_id, null from airport d1, airport d2 WHERE d1.airport_id <> d2.airport_id");

conn.execute("INSERT INTO flight (flight_id, route_id, departure_time, arrival_time, pilot_id, status) VALUES (1, 1, '2025-05-10 07:10', NULL, 2, 'Not departed')");

conn.commit()

print("Records created successfully")
print("Total number of rows created :", conn.total_changes)
print("\n");

# Functions #
# Menu functions
# choice = numerical value of the option chosen
# object = the string value of the option chosen

def showMainMenu():
    # Show main menu
    print("Choose what you want work with:")
    print("1) Flights")
    print("2) Pilots")
    print("3) Destinations")
    print("4) Exit")

    choice = input("Enter your option (mainmenu) \n")
    processMenuChoice(choice)

def processMenuChoice(choice):
    if choice == "1":
        print("Flights selected")
        showActionMenu("flight")
    elif choice == "2":
        print("Pilots selected")
        showActionMenu("pilot")
    elif choice == "3":
        print("Destinations selected")    
        showActionMenu("destination")
    elif choice == "4":
        print("Goodbye")
    else:
        print("Input not recognised, try again")   
        showMainMenu() 

def showActionMenu(object):
    print("Choose what you want to do:")
    print("1) View a " + object)
    print("2) Amend a " + object)
    print("3) Add a " + object)
    print("4) Delete a " + object)
    print("5) Back")
    choice = input("Enter your option (actionmenu) \n")
    processActionChoice(object, choice)

def processActionChoice(object, choice):
    print("Choice:" + str(choice))
    print("Object:" + object)    
    if choice == "1":
        print("View " + object + " selected")
        showViewMenu(object)
    elif choice == "2":
        print("Amend " + object + " selected")
        showAmendMenu(object)
    elif choice == "3":
        print("Add " + object + " selected")  
        showAddMenu(object)
    elif choice == "4":
        print("Delete " + object + " selected")
        showDeleteMenu(object)
    elif choice == "5":
        print("Back selected")
        showMainMenu()    
    else:
        print("Input not recognised, try again")    

def showViewMenu(object):
    print("Object:" + object)
    print("What do you want to search with:")
    print("1) Flight Code")
    print("2) Departure Location")
    print("3) Arrival Location")
    print("4) Pilot Name")
    print("5) Back")  
    choice = input("Enter your option (viewmenu) \n")
    processViewMenu(choice, object)

def processViewMenu(choice, object):
    print("Choice:" + str(choice))
    print("Object:" + object)
    if choice == "1":
        choice = input("Enter the Flight Code \n")
    elif choice == "2":
        choice = input("Enter the Departure Location \n")
    elif choice == "3":
        choice = input("Enter the Arrival Location \n")    
    elif choice == "4":
        choice = input("Enter the Pilot Name \n")
    elif choice == "5":
        showActionMenu(object)    
    else:
        print("Input not recognised, try again")  
    processChoice(choice)     

def processChoice(choice):
    returnData()

def showAmendMenu(object):
    print("What do you want to amend:")
    print("1) Flight Code")
    print("2) Departure Location")
    print("3) Arrival Location")
    print("4) Arrival Location")
    print("5) Back")    

def showAddMenu(object):
    print("What do you want to add:")
    print("1) Flight Code")
    print("2) Departure Location")
    print("3) Arrival Location")
    print("4) Arrival Location")
    print("5) Back")  
    

def showDeleteMenu(object):
    print("What do you want to delete:")
    print("1) Flight Code")
    print("2) Departure Location")
    print("3) Arrival Location")
    print("4) Arrival Location")
    print("5) Back")  


def returnData():
    cursor = conn.execute("SELECT flight_id, source.airport_name, dest.airport_name, departure_time, arrival_time, first_name, last_name, status \
        FROM flight, pilot, route, airport AS source, airport AS dest \
        WHERE flight.pilot_id = pilot.pilot_id AND route.route_id = flight.route_id AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id")

    for row in cursor:
       print("flight_id = ", row[0])
       print("departure = ", row[1])
       print("arrival = ", row[2])
       print("departure_time = ", row[3])
       print("arrival_time = ", row[4])  
       print("pilot = ", row[5]+" "+row[6])
       print("status = ", row[7], "\n")


# SQL DML functions

def updatePilot(firstname, lastname, id):
    conn.execute("UPDATE pilot SET first_name = '" + firstname + "', last_name = '" + lastname + "' WHERE pilot_id = " + id)
    conn.commit

def updateFlight(status, id):
    conn.execute("UPDATE flight SET status = '" + status + "' where flight_id = "+ id)    

def updateFlight(status, id):
    conn.execute("UPDATE flight SET status = '" + status + "' where flight_id = "+ id)    



# Start of UI application

showMainMenu()

