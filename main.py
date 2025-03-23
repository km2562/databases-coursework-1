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

def show_main_menu():
    # Show main menu
    print("===============================")
    print("Choose what you want work with:")
    print("1) Flights")
    print("2) Pilots")
    print("3) Destinations")
    print("4) Exit")

    choice = input("Enter your option (mainmenu) >> ")
    process_menu_choice(choice)

def process_menu_choice(choice):
    if choice == "1":
        print("Flights selected")
        show_action_menu("flight")
    elif choice == "2":
        print("Pilots selected")
        show_action_menu("pilot")
    elif choice == "3":
        print("Destinations selected")    
        show_action_menu("destination")
    elif choice == "4":
        print("Goodbye")
    else:
        print("Input not recognised, try again")   
        show_main_menu() 

def show_action_menu(object):
    print("===============================")
    print("Choose what you want to do:")
    print("1) View a " + object)
    print("2) Amend a " + object)
    print("3) Add a " + object)
    print("4) Delete a " + object)
    print("5) Back")
    choice = input("Enter your option (actionmenu) >> ")
    process_action_choice(object, choice)

def process_action_choice(object, choice):
    print("Choice:" + str(choice))
    print("Object:" + object)    
    if choice == "1":
        print("View " + object + " selected")
        show_view_menu(object)
    elif choice == "2":
        print("Amend " + object + " selected")
        show_amend_menu(object)
    elif choice == "3":
        print("Add " + object + " selected")  
        process_add_menu(object)
    elif choice == "4":
        print("Delete " + object + " selected")
        show_delete_menu(object)
    elif choice == "5":
        print("Back selected")
        show_main_menu()    
    else:
        print("Input not recognised, try again")    

def show_view_menu(object):
    print("Object:" + object)
    print("===============================")
    print("What do you want to search with:")
    print("1) Flight Code")
    print("2) Departure Location")
    print("3) Arrival Location")
    print("4) Pilot Name")
    print("5) Back")  
    choice = input("Enter your option (viewmenu) >> ")
    process_view_menu(choice, object)

def process_view_menu(choice, object):
    print("Choice:" + str(choice))
    print("Object:" + object)
    if choice == "1":
        value = input("Enter the Flight Code >> ")
        parameter = "flight_id"
    elif choice == "2":
        value = input("Enter the Departure Location >> ")
        parameter = "source.airport_code"
    elif choice == "3":
        value = input("Enter the Arrival Location >> ")    
        parameter = "dest.airport_code"
    elif choice == "4":
        value = input("Enter the Pilot Name >> ")
        parameter = "pilot.first_name"
    elif choice == "5":
        show_action_menu(object)    
    else:
        print("Input not recognised, try again")  
    process_choice(parameter, value)     

def process_choice(parameter, choice):
    return_data(parameter, choice)
    show_main_menu()

def show_amend_menu(object):
    print("===============================")    
    print("What do you want to amend:")
    print("1) Flight Code")
    print("2) Departure Location")
    print("3) Arrival Location")
    print("4) Arrival Location")
    print("5) Back")    


def add_flight():
    flight_code = input("Enter the Flight Code >> ")
    departure_airport = input("Enter the Departure Airport Code >> ")
    arrival_airport = input("Enter the Arrival Airport Code >> ")
    route_id = select_route(departure_airport, arrival_airport)
    print(route_id)
    departure_time_expected = input("Enter the Departure Time >> ")
    print("Choose from the following pilots:")
    get_pilot_list()
    pilot_id = input("Enter the Pilot >> ")
    print("Here")   

def add_airport():
    airport_code = input("Enter the Airport Code >> ")
    country = input("Enter the Country >> ")
    print("Here")    

def add_route():
    departure_airport_code = input("Enter the Departure Airport Code >> ")
    arrival_airport_code = input("Enter the Arrival Airport Code >> ")
    duration_minutes = input("Enter the Flight Duration >> ")
    print("Here")

def add_pilot():
    first_name = input("Enter the First Name >> ")
    last_name = input("Enter the Last Name >> ")
    date_hired = input("Enter the Hire Date >> ")
    print("Here")

def get_pilot_list():
    cursor = conn.execute("SELECT pilot_id, first_name + ' ' + last_name FROM pilot")
    for row in cursor:
        print(str(row[0]) + ") " + str(row[1]))

def validate_numeric_input():
    print("")

def validate_string_input():
    print("")

def validate_airport_input(airport_code):
    cursor = conn.execute("SELECT 1 FROM airport WHERE airport_code = '" + airport_code + "'")
    if cursor.arraysize == 1:
        return True
    else:
        return False   

def validate_pilot_input(name):
    cursor = conn.execute("SELECT 1 FROM flight WHERE first_name = '" + name + "'")
    if cursor.arraysize == 1:
        return True
    else:
        return False      
    print("")  

def validate_date_input(date):
    print("") 

def validate_flight_input(flight_code):
    cursor = conn.execute("SELECT 1 FROM pilot WHERE first_name  = '" + flight_code + "'")
    if cursor.arraysize == 1:
        return True
    else:
        return False          

def process_add_menu(choice):
    if choice == "flight":
        print("Flights selected")
        add_flight()
    elif choice == "airport":
        print("Airport selected")
        add_airport()
    elif choice == "route":
        print("Route selected")    
        add_route()
    elif choice == "pilot":
        print("Pilot selected")    
        add_pilot()        
    elif choice == "5":
        print("Goodbye")
    else:
        print("Input not recognised, try again")   
        show_main_menu()     



def show_delete_menu(object):
    print("Coming soon, no action taken")
    show_main_menu()
    

def return_data(parameter, value):
    cursor = conn.execute("SELECT flight_id, source.airport_name, dest.airport_name, departure_time, arrival_time, first_name, last_name, status \
                          FROM flight, pilot, route, airport AS source, airport AS dest \
                          WHERE flight.pilot_id = pilot.pilot_id AND route.route_id = flight.route_id \
                          AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id \
                          AND "+parameter+"= '"+value+"'")

    for row in cursor:
       print("flight_id = ", row[0])
       print("departure = ", row[1])
       print("arrival = ", row[2])
       print("departure_time = ", row[3])
       print("arrival_time = ", row[4])  
       print("pilot = ", row[5]+" "+row[6])
       print("status = ", row[7], "\n")


# SQL DML functions

def update_pilot(firstname, lastname, id):
    conn.execute("UPDATE pilot SET first_name = '" + firstname + "', last_name = '" + lastname + "' WHERE pilot_id = " + id)
    conn.commit

def update_flight(status, id):
    conn.execute("UPDATE flight SET status = '" + status + "' where flight_id = "+ id)    

def update_route(status, id):
    conn.execute("UPDATE route SET status = '" + status + "' where flight_id = "+ id)    

def insert_flight(flight_code, departure_airport_code, arrival_airport_code, departure_time_expected, pilot_id):
    conn.execute("INSERT INTO flight (flight_code, ) VALUES ('','','','','','','','','','')")

def select_route(departure_airport_code, arrival_airport_code):
    route = conn.execute("SELECT route_id FROM route, airport AS dep, airport AS arr \
                         WHERE route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id \
                         AND dep.airport_code = '"+departure_airport_code+"' \
                         AND arr.airport_code = '"+arrival_airport_code+"'")
    if route.arraysize == 1:
        for row in route:
            return row[0]
    else:
        return None

# Start of UI application

show_main_menu()

