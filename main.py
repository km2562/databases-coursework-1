import datetime
import re 
import sqlite3
from tabulate import tabulate

# ----------------------------- Database set up ---------------------------- #
conn = sqlite3.connect('flight_management')
print ("Database has been created")

conn.execute("DROP TABLE IF EXISTS flight")
conn.execute("DROP TABLE IF EXISTS pilot")
conn.execute("DROP TABLE IF EXISTS airport")
conn.execute("DROP TABLE IF EXISTS route")

conn.execute("CREATE TABLE flight (flight_id INTEGER PRIMARY KEY NOT NULL, flight_code VARCHAR(10), route_id INTEGER, departure_time_expected DATETIME, arrival_time_expected DATETIME, departure_time_actual DATETIME, arrival_time_actual DATETIME, pilot_id INTEGER, status VARCHAR(15))")
conn.execute("CREATE TABLE pilot (pilot_id INTEGER PRIMARY KEY NOT NULL, first_name VARCHAR(50), last_name VARCHAR(50), date_of_birth DATE, date_hired DATE)")
conn.execute("CREATE TABLE route (route_id INTEGER PRIMARY KEY NOT NULL, departure_airport_id INTEGER, arrival_airport_id INTEGER, duration_minutes INTEGER)")
conn.execute("CREATE TABLE airport (airport_id INTEGER PRIMARY KEY NOT NULL, airport_name VARCHAR(50), airport_code VARCHAR(3), country VARCHAR(50))")

print ("Tables created successfully")

# ----------------------------- Insert initial data ---------------------------- #

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

conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time_expected, arrival_time_expected, departure_time_actual, arrival_time_actual, pilot_id, status) \
              VALUES (1, 'FL1234', 1, '2025-05-10 07:10', '2025-05-10 10:10', NULL, NULL, 2, 'Not departed')");

conn.commit()

print("Records created successfully")
print("Total number of rows created :", conn.total_changes)
print("\n");

# ---------------------------- Functions ---------------------------------------- #
# -------------------------- Menu Functions ------------------------------------- #
# choice = numerical value of the option chosen
# object = the string value of the option chosen

def show_main_menu():
    # Show main menu
    print("===============================")
    print("Choose what you want work with:")
    print("1) Flights")
    print("2) Pilots")
    print("3) Destinations")
    print("4) Routes")
    print("5) Exit")

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
        print("Routes selected")    
        show_action_menu("route")        
    elif choice == "5":
        print("Goodbye")
    else:
        print("Input not recognised, try again 1")   
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
        print("Input not recognised, try again 2")    

def show_view_menu(object):
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
        parameter = "flight_code"
    elif choice == "2":
        value = input("Enter the Departure Location >> ")
        parameter = "source.airport_code"
    elif choice == "3":
        value = input("Enter the Arrival Location >> ")    
        parameter = "dest.airport_code"
    elif choice == "4":
        get_pilot_list()
        value = input("Enter the Pilot >> ")
        parameter = "pilot.pilot_id"
    elif choice == "5":
        show_action_menu(object)    
    else:
        print("Input not recognised, try again 3")  
    process_choice(parameter, value)     

def process_choice(parameter, choice):
    return_data(parameter, choice)
    show_main_menu()

def show_amend_menu(object):
    print("===============================")    
    print("What do you want to amend:")
    if object == "flight":
        show_amend_flight_menu()
    if object == "route":
        show_amend_route_menu()  
    if object == "destination":
        show_amend_destination_menu()     
    if object == "pilot":
        show_amend_pilot_menu()                 

def show_amend_flight_menu():
    print("Choose a flight to amend")
    get_flight_list()
    id = input("Enter the Flight ID >> ")
    return_data("flight_id", id)
    print("Choose a value to update")
    print("1) Departure Time")
    print("2) Arrival Time")
    print("3) Flight Status")
    print("4) Back") 
    choice = input("Enter your option (amendmenuflight) >> ")
    process_amend_flight_menu(choice, id) 

def process_amend_flight_menu(choice, id):
    if choice == "1":
        value = input("Enter the Departure Time >> ")    
        parameter = "departure_time_actual"
    elif choice == "2":
        value = input("Enter the Arrival Time >> ")
        parameter = "arrival_time_actual"
        update_flight()
    elif choice == "3":
        value = input("Enter the Flight Status >> ")    
        parameter = "status"
        update_flight()
    elif choice == "4":
        show_action_menu("flight")    
    else:
        print("Input not recognised, try again 3")  
    update_flight(parameter, value, id)
    show_main_menu()  

def show_amend_route_menu():
    print("Choose a route to amend")
    get_route_list()
    id = input("Enter the Route ID >> ")
    return_data("route.route_id", id)    
    print("1) Duration")
    print("2) Back")  
    choice = input("Enter your option (amendmenuroute) >> ")
    process_amend_route_menu(choice, id) 

def process_amend_route_menu(choice, id):
    if choice == "1":
        value = input("Enter the Duration >> ")    
        parameter = "duration_minutes"
    elif choice == "2":
        show_action_menu("route")    
    else:
        print("Input not recognised, try again 3")  
    update_route(parameter, value, id)   
    show_main_menu()  

def show_amend_destination_menu():
    print("Choose an airport to amend")
    get_airport_list()
    id = input("Enter the Airport ID >> ")
    print("1) Airport Name")
    print("4) Back")  
    choice = input("Enter your option (amendmenudestination) >> ")
    process_amend_destination_menu(choice, id)    

def process_amend_destination_menu(choice, id):
    if choice == "1":
        value = input("Enter the Airport Name >> ")    
        parameter = "airport_name"
    elif choice == "2":
        show_action_menu("destination")    
    else:
        print("Input not recognised, try again 3")  
    update_route(parameter, value, id)  
    show_main_menu()  

def show_amend_pilot_menu():
    print("Choose a pilot to amend")
    get_pilot_list()
    id = input("Enter the Pilot ID >> ")
    print("1) First Name")
    print("2) Last Name")
    print("3) Back")   
    choice = input("Enter your option (amendmenupilot) >> ")
    process_amend_pilot_menu(choice, id)       

def process_amend_pilot_menu(choice, id):
    if choice == "1":
        value = input("Enter the First Name >> ")    
        parameter = "first_name"
    elif choice == "2":
        value = input("Enter the Last Name >> ")    
        parameter = "last_name"        
    elif choice == "3":
        show_action_menu("pilot")    
    else:
        print("Input not recognised, try again 3")  
    update_pilot(parameter, value, id)  
    show_main_menu()        

def add_flight():
    flight_code = input("Enter the Flight Code >> ")
    route_not_valid = True
    attempts = 0
    while route_not_valid and attempts <= 3:
        departure_airport = input("Enter the Departure Airport Code >> ")
        arrival_airport = input("Enter the Arrival Airport Code >> ")
        route_id = get_route_id(departure_airport, arrival_airport)                 # Derive route_id
        if route_id == None:
            print("Route "+ str(departure_airport) +" to "+ str(arrival_airport)+" not found, try again")
            attempts = attempts+1
        else:
            route_not_valid = False    
    if attempts>=3:
        print("Too many incorrect inputs, return to main menu")
        show_main_menu()        
    departure_time_expected = input("Enter the Departure Time >> ")
    validate_date_input(departure_time_expected)
    print("Choose from the following pilots:")
    get_pilot_list()
    pilot_id = input("Enter the Pilot >> ")
    insert_flight(flight_code, route_id, departure_time_expected, pilot_id)
    show_main_menu()   

def add_airport():
    airport_code = input("Enter the Airport Code >> ")
    airport_name = input("Enter the Airport Name >> ")
    country = input("Enter the Country >> ")
    insert_airport(airport_code, airport_name, country)

def add_route():
    airport_exists = False
    attempts = 0
    while airport_exists == False and attempts <= 3:
        departure_airport_code = input("Enter the Departure Airport Code >> ")
        airport_exists = validate_airport_input(departure_airport_code)    
        print(departure_airport_code)   
        print(airport_exists)         
        if airport_exists == False:
            print(str(departure_airport_code) +" not found, try again")
            attempts = attempts+1
        else:
            departure_airport_id = get_airport_id(departure_airport_code)
            airport_exists = True   
            attempts = 0 
    if attempts>=3:
        print("Too many incorrect inputs, return to main menu")
        show_main_menu()  
    airport_exists = False    
    while airport_exists == False and attempts <= 3:
        arrival_airport_code = input("Enter the Arrival Airport Code >> ")
        airport_exists = validate_airport_input(arrival_airport_code)                
        if airport_exists == False:
            print(str(arrival_airport_code) +" not found, try again")
            attempts = attempts+1
        else:
            arrival_airport_id = get_airport_id(arrival_airport_code)
            airport_exists = True  
            attempts = 0        
    if attempts>=3:
        print("Too many incorrect inputs, return to main menu")
        show_main_menu()  
    duration_minutes = input("Enter the Flight Duration >> ")
    insert_route(departure_airport_id, arrival_airport_id, duration_minutes)

def add_pilot():
    first_name = input("Enter the First Name >> ")
    last_name = input("Enter the Last Name >> ")
    date_hired = input("Enter the Hire Date >> ")
    insert_pilot(first_name, last_name, date_hired)


# -------------------------- Validation Functions ------------------------------------- #

def validate_numeric_input():
    print("")

def validate_string_input():
    print("")

def validate_airport_input(airport_code):
    cursor = conn.execute("SELECT 1 FROM airport WHERE airport_code = '" + airport_code + "'")
    print(convert_to_table(cursor))
    if cursor.rowcount == 1:
        return True
    else:
        return False   

def validate_pilot_input(name):
    cursor = conn.execute("SELECT 1 FROM flight WHERE first_name = '" + name + "'")
    if cursor.rowcount == 1:
        return True
    else:
        return False       

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
    elif choice == "destination":
        print("Destination selected")
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
        print("Input not recognised, try again 4")   
        show_main_menu()     



def show_delete_menu(object):
    print("Coming soon, no action taken")
    show_main_menu()
    

def calculate_arrival_time(departure_time, duration):
    split_date = re.split('[- :]', departure_time)
    date_and_time = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), int(split_date[3]), int(split_date[4]), int(split_date[5]))    
    time_change = datetime.timedelta(minutes=duration) 
    arrival_time = date_and_time + time_change 
    return str(arrival_time)


def return_data(parameter, value):
    print("Parameter: " + str(parameter))
    print("Value: " + str(value))
    cursor = conn.execute("SELECT flight_code AS [Flight Code], source.airport_name AS [Departure Airport], dest.airport_name AS [Arrival Airport], \
                          IFNULL(departure_time_actual,departure_time_expected) AS [Departure Time], IFNULL(arrival_time_actual,arrival_time_expected) AS [Arrival Time], first_name || ' ' || last_name AS [Pilot Name], status AS [Status] \
                          FROM flight, pilot, route, airport AS source, airport AS dest \
                          WHERE flight.pilot_id = pilot.pilot_id AND route.route_id = flight.route_id \
                          AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id \
                          AND "+str(parameter)+" = '"+str(value)+"'")
    
    print("===============================")
    table = convert_to_table(cursor)
    print(table)



# -------------------------- SQL DML Functions ------------------------------------- #

def update_pilot(firstname, lastname, id):
    conn.execute("UPDATE pilot SET first_name = '" + firstname + "', last_name = '" + lastname + "' WHERE pilot_id = " + id)
    conn.commit
    print("Update successful") 

def update_flight(parameter, value, id):
    conn.execute("UPDATE flight SET "+parameter+" = '" + value + "' where flight_id = "+ id)    
    conn.commit
    print("Update successful")           

def update_route(parameter, value, id):
    conn.execute("UPDATE route SET "+parameter+" = '" + value + "' where route_id = "+ id)   
    conn.commit
    print("Update successful")       

def insert_flight(flight_code, route_id, departure_time_expected, pilot_id):
    conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time_expected, pilot_id, status) \
                 VALUES (NULL, '"+str(flight_code)+"','"+str(route_id)+"','"+str(departure_time_expected)+"','"+str(pilot_id)+"', 'On Time')")
    conn.commit
    print("Insert successful")


def insert_airport(airport_code, airport_name, country):
    conn.execute("INSERT INTO airport (airport_id, airport_code, airport_name, country) \
                 VALUES (NULL, '"+airport_code+"','"+airport_name+"','"+country+"')")
    conn.commit
    print("Insert successful")    

def insert_pilot(first_name, last_name, date_hired):
    conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) \
                 VALUES (NULL, '"+first_name+"','"+last_name+"','"+date_hired+"')")
    conn.commit
    print("Insert successful")    

def insert_route(departure_airport_id, arrival_airport_id, duration_minutes):
    conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) \
                 VALUES (NULL, '"+str(departure_airport_id)+"','"+str(arrival_airport_id)+"','"+str(duration_minutes)+"')")
    conn.commit
    print("Insert successful")        


def get_route_id(departure_airport_code, arrival_airport_code):
    route = conn.execute("SELECT route_id FROM route, airport AS dep, airport AS arr \
                         WHERE route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id \
                         AND dep.airport_code = '"+departure_airport_code+"' \
                         AND arr.airport_code = '"+arrival_airport_code+"'")
    if route.arraysize == 1:
        for row in route:
            return row[0]
    else:
        return None

def get_airport_id(airport_code):
    airport = conn.execute("SELECT airport_id FROM airport WHERE airport_code = '"+airport_code+"'")
    if airport.arraysize == 1:
        for row in airport:
            return row[0]
    else:
        return None

def get_flight_list():
    flight = conn.execute("SELECT flight_id AS [Flight ID], flight_code AS [Flight Code] FROM flight")
    print(convert_to_table(flight))    

def get_route_list():
    route = conn.execute("SELECT route_id AS [Route ID], dep.airport_code AS [Departure Airport], arr.airport_code AS [Arrival Airport] FROM route, airport AS dep, airport AS arr \
                         WHERE route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id")
    print(convert_to_table(route))   

def get_pilot_list():
    pilot = conn.execute("SELECT pilot_id AS [Pilot ID], first_name || ' ' || last_name AS [Pilot Name] FROM pilot")
    print(convert_to_table(pilot))   

def get_airport_list():
    airport = conn.execute("SELECT airport_id AS [Airport ID], airport_name AS [Airport Name], airport_code AS [Airport Code], country AS [Country] FROM airport")
    print(convert_to_table(airport))        

def convert_to_table(data):
    table = tabulate(data, headers="keys", tablefmt="pipe")
    return table

# -------------------------- Start of UI application ------------------------------------- #

show_main_menu()

