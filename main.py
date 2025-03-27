from datetime import datetime, timedelta, date
import re 
import sqlite3
from tabulate import tabulate

# ----------------------------- Database set up ---------------------------- #
conn = sqlite3.connect('flight_management')
print ("Database has been created")

conn.execute("DROP TABLE IF EXISTS flight;")
conn.execute("DROP TABLE IF EXISTS pilot;")
conn.execute("DROP TABLE IF EXISTS airport;")
conn.execute("DROP TABLE IF EXISTS route;")

conn.execute("CREATE TABLE airport (airport_id INTEGER PRIMARY KEY NOT NULL, airport_name VARCHAR(50), airport_code VARCHAR(3), country VARCHAR(50))")
conn.execute("CREATE TABLE pilot (pilot_id INTEGER PRIMARY KEY NOT NULL, first_name VARCHAR(50), last_name VARCHAR(50), date_of_birth DATE, date_hired DATE)")
conn.execute("CREATE TABLE route (route_id INTEGER PRIMARY KEY NOT NULL, departure_airport_id INTEGER, arrival_airport_id INTEGER, duration_minutes INTEGER)")
conn.execute("CREATE TABLE flight (flight_id INTEGER PRIMARY KEY NOT NULL, flight_code VARCHAR(10), route_id INTEGER, departure_time DATETIME, arrival_time, pilot_id INTEGER, status VARCHAR(15));")

print ("Tables created successfully")

# ----------------------------- Insert initial data ---------------------------- #

conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (1, 'Joseph','Walters','1970-05-06','2015-06-17');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (2, 'Jo','Walters','1989-12-08','2022-05-31');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (3, 'Alan','Thomson','1981-08-05','2007-12-17');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (4, 'Ian','Jackson','1988-12-26','2022-04-14');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (5, 'Samantha','North','1973-10-27','2013-07-19');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (6, 'Austin','Redman','1980-09-25','2024-11-27');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (7, 'Bruce','Crowther','1981-11-08','2007-06-16');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (8, 'Peter','Newman','1983-06-10','2017-09-19');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (9, 'George','Langford','1987-09-11','2022-05-03');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) VALUES (10, 'Nina','Palmer','1976-04-13','2016-05-14');")

#https://www.iata.org/en/publications/directories/code-search/?
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (1, 'London Gatwick', 'LGW', 'UK');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (2, 'London Luton', 'LTN', 'UK');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (3, 'London Heathrow', 'LHR', 'UK');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (4, 'Split', 'SPU', 'Croatia');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (5, 'Corfu', 'CFU', 'Greece');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (6, 'Pula', 'PUY', 'Croatia');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (7, 'Paris Orly', 'ORY', 'France');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (8, 'Berlin Brandenburg', 'BER', 'Germany');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (9, 'Brussels', 'BRU', 'Belgium');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (10, 'New York John F Kennedy Intl', 'JFK', 'USA');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (11, 'New York Newark Liberty Intl', 'EWR', 'USA');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (12, 'Lisbon', 'LIS', 'Portugal');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (13, 'Milan Bergamo/Orio al Serio', 'BGY', 'Italy');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (14, 'Rome Griffiss Intl', 'RME', 'Italy');")
conn.execute("INSERT INTO airport (airport_id, airport_name, airport_code, country) VALUES (15, 'Malaga Airport', 'AGP', 'Spain');")

# LGW ->
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (1, 1, 4, 139);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (2, 1, 5, 178);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (3, 1, 6, 121);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (4, 1, 7, 52);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (5, 1, 8, 100);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (6, 1, 9, 52);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (7, 1, 10, 443);")

# <- LGW
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (8, 4, 1, 139);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (9, 5, 1, 178);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (10, 6, 1, 121);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (11, 7, 1, 52);")

conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, pilot_id, status) VALUES (1, 'FL1234', 1, '2025-05-10 07:10', 2, 'Not departed');")
conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, pilot_id, status) VALUES (2, 'FL4321', 8, '2025-05-11 10:50', 2, 'Not departed');")
conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, pilot_id, status) VALUES (3, 'FL2345', 2, '2025-05-11 08:30', 1, 'Not departed');")
conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, pilot_id, status) VALUES (4, 'FL5432', 9, '2025-05-12 09:15', 1, 'Not departed');")

# Calculate arrival times for all flights using the duration_minutes from route
conn.execute("UPDATE flight SET arrival_time = DATETIME(departure_time, '+' || (SELECT duration_minutes FROM route WHERE flight.route_id = route.route_id) || ' minute') WHERE 1=1")

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
        exit()
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
    print("5) Go back")
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
        show_action_menu(object)  

def show_view_menu(object):
    print("===============================")
    print("What do you want to search with:")
    print("1) Flight Code")
    print("2) Departure Location")
    print("3) Arrival Location")
    print("4) Pilot Name")
    print("5) Departure Date")
    print("6) Arrival Date")
    print("7) Go back")  
    choice = input("Enter your option (viewmenu) >> ")
    process_view_menu(choice, object)

def process_view_menu(choice, object):
    print("Choice:" + str(choice))
    print("Object:" + object)
    if choice == "1":
        value = input("Enter the Flight Code >> ")
        column = "flight_code"
    elif choice == "2":
        value = input("Enter the Departure Location >> ")
        column = "source.airport_code"
    elif choice == "3":
        value = input("Enter the Arrival Location >> ")    
        column = "dest.airport_code"
    elif choice == "4":
        display_pilot_list()
        value = input("Enter the Pilot >> ")
        column = "pilot.pilot_id"        
    elif choice == "5":
        value = input("Enter the Departure Day (format YYYY-MM-DD) >> ")
        if not validate_date_input(value, "%Y-%m-%d"):
            print("Input not recognised, try again")
            process_view_menu(choice, object)
        else:
            column = "flight.departure_time"
    elif choice == "6":
        value = input("Enter the Arrival Day (format YYYY-MM-DD) >> ")
        if not validate_date_input(value, "%Y-%m-%d"):
            print("Input not recognised, try again")
            process_view_menu(choice, object)
        else:
            column = "flight.arrival_time_expected"
    elif choice == "7":
        show_action_menu(object)    
    else:
        print("Input not recognised, try again 3")
        show_view_menu(object)  
    process_view_choice(column, value)     

def process_view_choice(column, value):
    if "time" in column:
        display_flight_data_for_day(column, value)
    else:
        display_flight_data(column, value)
    show_main_menu()

def show_amend_menu(object):
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
    display_flight_list()
    id = input("Enter the Flight ID >> ")
    if validate_numeric_input(id):
        display_flight_data("flight_id", id)
        print("Choose a value to update")
        print("1) Departure Time")
        print("2) Arrival Time")
        print("3) Flight Status")
        print("4) Go back") 
        choice = input("Enter your option (amendmenuflight) >> ")
        process_amend_flight_menu(choice, id) 
    else:
        print("Input not recognised, try again")    
        show_amend_flight_menu()    

def process_amend_flight_menu(choice, id):
    if choice == "1":
        value = input("Enter the Departure Time >> ")    
        column = "departure_time"
    elif choice == "2":
        value = input("Enter the Arrival Time >> ")
        column = "arrival_time"
        update_flight()
    elif choice == "3":
        value = input("Enter the Flight Status >> ")    
        column = "status"
        update_flight()
    elif choice == "4":
        show_action_menu("flight")    
    else:
        print("Input not recognised, try again 3")  
    update_flight(column, value, id)
    show_main_menu()  

def show_amend_route_menu():
    print("Choose a route to amend")
    display_route_list()
    id = input("Enter the Route ID >> ")
    if validate_numeric_input(id):
        display_flight_data("route.route_id", id)    
        print("1) Duration")
        print("2) Go back")  
        choice = input("Enter your option (amendmenuroute) >> ")
        process_amend_route_menu(choice, id) 
    else:
        print("Input not recognised, try again")    
        show_amend_route_menu()         

def process_amend_route_menu(choice, id):
    if choice == "1":
        value = input("Enter the Duration >> ")    
        column = "duration_minutes"
    elif choice == "2":
        show_action_menu("route")    
    else:
        print("Input not recognised, try again 3")  
    update_route(column, value, id)   
    show_main_menu()  

def show_amend_destination_menu():
    print("Choose an airport to amend: ")
    display_airport_list()
    id = input("Enter the Airport ID >> ")
    if validate_numeric_input(id):
        print("1) Airport Name")
        print("2) Go back")  
        choice = input("Enter your option (amendmenudestination) >> ")
        process_amend_destination_menu(choice, id)    
    else:
        print("Input not recognised, try again")    
        show_amend_destination_menu() 

def process_amend_destination_menu(choice, id):
    if choice == "1":
        value = input("Enter the Airport Name >> ")    
        column = "airport_name"
    elif choice == "2":
        show_action_menu("destination")    
    else:
        print("Input not recognised, try again 3")  
    update_route(column, value, id)  
    show_main_menu()  

def show_amend_pilot_menu():
    print("Choose a pilot to amend")
    display_pilot_list()
    id = input("Enter the Pilot ID >> ")
    if validate_numeric_input(id):
        print("1) First Name")
        print("2) Last Name")
        print("3) Go back")   
        choice = input("Enter your option (amendmenupilot) >> ")
        process_amend_pilot_menu(choice, id)      
    else:
        print("Input not recognised, try again")    
        show_amend_pilot_menu() 

def process_amend_pilot_menu(choice, id):
    if choice == "1":
        value = input("Enter the First Name >> ")    
        column = "first_name"
    elif choice == "2":
        value = input("Enter the Last Name >> ")    
        column = "last_name"        
    elif choice == "3":
        show_action_menu("pilot")    
    else:
        print("Input not recognised, try again 3")  
    update_pilot(column, value, id)  
    show_main_menu()        

def process_add_menu(object):
    if object == "flight":
        print("Flights selected")
        add_flight()
    elif object == "destination":
        print("Destination selected")
        add_airport()
    elif object == "route":
        print("Route selected")    
        add_route()
    elif object == "pilot":
        print("Pilot selected")    
        add_pilot()        
    else:
        print("Input not recognised, try again 4")   
        show_main_menu()    

def add_flight():
    flight_code = input("Enter the Flight Code >> ")
    if validate_flight_exists(flight_code):
        print("Flight already exists, no action taken")
        show_main_menu()
    else:    
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
        departure_time = input("Enter the Departure Time (format YYYY-MM-DD HH:MM) >> ")
        if validate_date_input(departure_time, "%Y-%m-%d %H:%M"):
            print("Choose from the following pilots:")
            display_pilot_list()
            pilot_id = input("Enter the Pilot ID >> ")
            insert_flight(flight_code, route_id, departure_time, pilot_id)
            show_main_menu()   
        else: 
            print("Input not recognised, start again")
            add_flight()
    show_main_menu()               


def add_airport():
    airport_code = input("Enter the Airport Code >> ")
    if validate_airport_input(airport_code):
        print("Airport already exists, no action taken")
        show_main_menu()
    else:    
        airport_name = input("Enter the Airport Name >> ")
        country = input("Enter the Country >> ")
        insert_airport(airport_code, airport_name, country)
    show_main_menu()       

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
    if validate_route_exists(departure_airport_id, arrival_airport_id):    
        print("Route already exists, no action taken")
        show_main_menu
    else:    
        duration_minutes = input("Enter the Flight Duration >> ")
        if validate_numeric_input(duration_minutes):
            insert_route(departure_airport_id, arrival_airport_id, duration_minutes)
        else:
            print("Invalid input, start again")
            add_route()  
    show_main_menu()        


def add_pilot():
    first_name = input("Enter the First Name >> ")
    last_name = input("Enter the Last Name >> ")
    date_of_birth = input("Enter the Date of Birth (format YYYY-MM-DD) >> ")
    if validate_date_input(date_of_birth, "%Y-%m-%d"):
        date_hired = input("Enter the Hire Date (format YYYY-MM-DD) >> ")
        if validate_date_input(date_hired, "%Y-%m-%d"):
            insert_pilot(first_name, last_name, date_of_birth, date_hired)
    else:
        print("Date not recognised, start again")   
        add_pilot()
    show_main_menu()

def show_delete_menu(object):
    print("Coming soon, no action taken")
    show_main_menu()

# -------------------------- Validation Functions ------------------------------------- #

def validate_numeric_input(value):
    return value.isnumeric()

def validate_string_input():
    print("")

def validate_airport_input(airport_code):
    cursor = conn.execute("SELECT '1' AS [Found] FROM airport WHERE airport_code = '" + airport_code + "';")
    for row in cursor:
        if row[0] == "1":
            return True
    return False   

def validate_pilot_input(name):
    cursor = conn.execute("SELECT '1' AS [Found] FROM pilot WHERE first_name = '" + name + "';")
    for row in cursor:
        if row[0] == "1":
            return True
    return False

def validate_route_exists(departure_airport_id, arrival_airport_id):
    cursor = conn.execute("SELECT '1' AS [Found] FROM route WHERE departure_airport_id = '"+str(departure_airport_id)+"' AND arrival_airport_id = '"+str(arrival_airport_id)+"';")
    for row in cursor:
        if row[0] == "1":
            return True
    return False

def validate_flight_exists(flight_code):
    cursor = conn.execute("SELECT '1' AS [Found] FROM flight WHERE flight_code = '"+str(flight_code)+"';")
    for row in cursor:
        if row[0] == "1":
            return True
    return False

def validate_date_input(date, format):
    valid = True
    try:
        valid = bool(datetime.strptime(date, format))
    except ValueError:
        valid = False
    return valid    

def validate_flight_input(flight_code):
    cursor = conn.execute("SELECT '1' AS [Found] FROM flight WHERE flight_code  = '" + flight_code + "';")
    for row in cursor:
        if row[0] == "1":
            return True
    return False           

# ---------------------------- Transformations ------------------------------------- #   

def calculate_arrival_time(departure_time, duration):
    split_date = re.split('[- :]', departure_time)
    date_and_time = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), int(split_date[3]), int(split_date[4]), 0)
    time_change = timedelta(minutes=duration) 
    arrival_time = date_and_time + time_change 
    return str(arrival_time)

def convert_to_table(data):
    table = tabulate(data, headers="keys", tablefmt="pipe")
    return table

def exit():
    print("Goodbye")

# -------------------------- SQL DML Functions ------------------------------------- #

# ------------------------------- Update ------------------------------------------- #

def update_pilot(column, value, id):
    conn.execute("UPDATE pilot SET "+column+" = '" + value + "' WHERE pilot_id = " + id +";")
    conn.commit()
    print("Update successful") 

def update_flight(column, value, id):
    conn.execute("UPDATE flight SET "+column+" = '" + value + "' where flight_id = "+ id +";")    
    conn.commit()
    print("Update successful")           

def update_route(column, value, id):
    conn.execute("UPDATE route SET "+column+" = '" + value + "' where route_id = "+ id +";")   
    conn.commit()
    print("Update successful")    

def update_airport(column, value, id):
    conn.execute("UPDATE airport SET "+column+" = '" + value + "' where route_id = "+ id +";")   
    conn.commit()
    print("Update successful")        

# ------------------------------- Insert ------------------------------------------- #

def insert_flight(flight_code, route_id, departure_time, pilot_id):
    duration_minutes = get_duration_minutes(route_id)
    arrival_time = calculate_arrival_time(departure_time, duration_minutes)
    conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, arrival_time, pilot_id, status) \
                 VALUES (NULL, '"+str(flight_code)+"','"+str(route_id)+"','"+str(departure_time)+"','"+str(arrival_time)+"','"+str(pilot_id)+"', 'On Time');")
    conn.commit()
    print("Insert successful")

def insert_airport(airport_code, airport_name, country):
    conn.execute("INSERT INTO airport (airport_id, airport_code, airport_name, country) \
                 VALUES (NULL, '"+airport_code+"','"+airport_name+"','"+country+"');")
    conn.commit()
    print("Insert successful")    

def insert_pilot(first_name, last_name, date_of_birth, date_hired):
    conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_of_birth, date_hired) \
                 VALUES (NULL, '"+first_name+"','"+last_name+"','"+date_of_birth+"','"+date_hired+"');")
    conn.commit()
    print("Insert successful")    

def insert_route(departure_airport_id, arrival_airport_id, duration_minutes):
    conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) \
                 VALUES (null, "+str(departure_airport_id)+","+str(arrival_airport_id)+","+str(duration_minutes)+");")
    conn.commit()
    print("Insert successful")        

# ------------------------------- Select ------------------------------------------- #

def get_route_id(departure_airport_code, arrival_airport_code):
    route = conn.execute("SELECT route_id FROM route, airport AS dep, airport AS arr \
                         WHERE route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id \
                         AND dep.airport_code = '"+departure_airport_code+"' \
                         AND arr.airport_code = '"+arrival_airport_code+"';")
    for row in route:
        return row[0]
    return None

def get_duration_minutes(route_id):
    route = conn.execute("SELECT duration_minutes FROM route WHERE route_id = '"+str(route_id)+"';")
    for row in route:
        return row[0]
    return None        

def get_airport_id(airport_code):
    airport = conn.execute("SELECT airport_id FROM airport WHERE airport_code = '"+airport_code+"';")
    for row in airport:
        return row[0]
    return None

def get_flight_count(column, value):
    flight = conn.execute("SELECT COUNT(*) \
                          FROM flight, pilot, route, airport AS source, airport AS dest \
                          WHERE flight.pilot_id = pilot.pilot_id AND route.route_id = flight.route_id \
                          AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id \
                          AND "+str(column)+" = "+str(value)+";")    
    for row in flight:
        return row[0]
    return None

def get_route(column, value):
    route = conn.execute("SELECT route_id AS [Route ID], dep.airport_code AS [Departure Airport], arr.airport_code AS [Arrival Airport] FROM route, airport AS dep, airport AS arr \
                         WHERE route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id AND "+column+" = '"+str(value)+"';")
    print(convert_to_table(route))   

def display_flight_list():
    flight = conn.execute("SELECT flight_id AS [Flight ID], flight_code AS [Flight Code] FROM flight;")
    print(convert_to_table(flight))    

def display_route_list():
    route = conn.execute("SELECT route_id AS [Route ID], dep.airport_code AS [Departure Airport], arr.airport_code AS [Arrival Airport] FROM route, airport AS dep, airport AS arr \
                         WHERE route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id;")
    print(convert_to_table(route))   

def display_pilot_list():
    pilot = conn.execute("SELECT pilot_id AS [Pilot ID], first_name || ' ' || last_name AS [Pilot Name] FROM pilot;")
    print(convert_to_table(pilot))   

def display_airport_list():
    airport = conn.execute("SELECT airport_id AS [Airport ID], airport_name AS [Airport Name], airport_code AS [Airport Code], country AS [Country] FROM airport;")
    print(convert_to_table(airport))     

def display_flight_data_for_day(column, date_value):
    split_date = re.split('[- :]', date_value)
    start_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    add_day = timedelta(days=1)
    end_date = start_date+add_day
    flight = conn.execute("SELECT flight_code AS [Flight Code], source.airport_name AS [Departure Airport], dest.airport_name AS [Arrival Airport], \
                          departure_time AS [Departure Time], arrival_time AS [Arrival Time], first_name || ' ' || last_name AS [Pilot Name], status AS [Status] \
                          FROM flight, pilot, route, airport AS source, airport AS dest \
                          WHERE flight.pilot_id = pilot.pilot_id AND route.route_id = flight.route_id \
                          AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id \
                          AND "+str(column)+" BETWEEN '"+str(start_date)+"' AND '"+str(end_date)+"';")   
    print(convert_to_table(flight))


def display_flight_data(column, value):
    print("Column: " + str(column))
    print("Value: " + str(value))
    string_output = "SELECT flight_code AS [Flight Code], source.airport_name AS [Departure Airport], dest.airport_name AS [Arrival Airport], \
                          departure_time AS [Departure Time], arrival_time AS [Arrival Time], first_name || ' ' || last_name AS [Pilot Name], status AS [Status] \
                          FROM flight, pilot, route, airport AS source, airport AS dest \
                          WHERE flight.pilot_id = pilot.pilot_id AND route.route_id = flight.route_id \
                          AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id \
                          AND "+str(column)+" = '"+str(value)+"';"
    #print(str(string_output))

    flight = conn.execute("SELECT flight_code AS [Flight Code], source.airport_name AS [Departure Airport], dest.airport_name AS [Arrival Airport], \
                          departure_time AS [Departure Time], arrival_time AS [Arrival Time], first_name || ' ' || last_name AS [Pilot Name], status AS [Status] \
                          FROM flight, pilot, route, airport AS source, airport AS dest \
                          WHERE flight.pilot_id = pilot.pilot_id AND route.route_id = flight.route_id \
                          AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id \
                          AND "+str(column)+" = '"+str(value)+"';")                      
    
    print("===============================")
    table = convert_to_table(flight)
    print(table)

# -------------------------- Start of UI application ------------------------------------- #

print(get_route("dep.airport_code", "LGW"))
show_main_menu()

