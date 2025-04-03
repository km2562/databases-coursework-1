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
conn.execute("DROP VIEW IF EXISTS flight_and_pilot;")

conn.execute("CREATE TABLE airport (airport_id INTEGER PRIMARY KEY NOT NULL, airport_name VARCHAR(50) NOT NULL, airport_code VARCHAR(3) NOT NULL, country VARCHAR(50) NOT NULL)")
conn.execute("CREATE TABLE pilot (pilot_id INTEGER PRIMARY KEY NOT NULL, first_name VARCHAR(50) NOT NULL, last_name VARCHAR(50) NOT NULL, pilot_name VARCHAR(100) GENERATED ALWAYS AS (first_name || ' ' || last_name) VIRTUAL NOT NULL, date_hired DATE NULL)")
conn.execute("CREATE TABLE route (route_id INTEGER PRIMARY KEY NOT NULL, departure_airport_id INTEGER REFERENCES airport(airport_id) NOT NULL, arrival_airport_id INTEGER REFERENCES airport(airport_id) NOT NULL, duration_minutes INTEGER NOT NULL)")
conn.execute("CREATE TABLE flight (flight_id INTEGER PRIMARY KEY NOT NULL, flight_code VARCHAR(10) NOT NULL, route_id INTEGER REFERENCES route(route_id) NOT NULL, departure_time DATETIME NOT NULL, arrival_time DATETIME NULL, pilot_id INTEGER REFERENCES pilot(pilot_id) NULL, status VARCHAR(15) DEFAULT 'Not departed' NULL);")

print ("Tables created successfully")

# ---------------------------Create Views --------------------------------#

conn.execute("CREATE VIEW flight_and_pilot AS SELECT flight_id, flight_code, route_id, departure_time, arrival_time, IFNULL(pilot.pilot_id, 'Unassigned') AS [pilot_id], IFNULL(pilot_name, 'Unassigned') AS [pilot_name], date_hired, status FROM flight LEFT JOIN pilot ON flight.pilot_id = pilot.pilot_id")

# ----------------------------- Insert initial data ---------------------------- #

conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (1, 'Joseph','Walters','2015-06-17');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (2, 'Jo','Walters','2022-05-31');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (3, 'Alan','Thomson','2007-12-17');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (4, 'Ian','Jackson','2022-04-14');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (5, 'Samantha','North','2013-07-19');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (6, 'Austin','Redman','2024-11-27');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (7, 'Bruce','Crowther','2007-06-16');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (8, 'Peter','Newman','2017-09-19');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (9, 'George','Langford','2022-05-03');")
conn.execute("INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (10, 'Nina','Palmer','2016-05-14');")

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

conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (1, 1, 4, 139);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (2, 1, 5, 178);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (3, 1, 6, 121);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (4, 1, 7, 52);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (5, 1, 8, 100);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (6, 1, 9, 52);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (7, 1, 10, 443);")

conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (8, 4, 1, 139);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (9, 5, 1, 178);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (10, 6, 1, 121);")
conn.execute("INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (11, 7, 1, 52);")

conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, pilot_id) VALUES (1, 'FL1234', 1, '2025-05-10 07:10', NULL);")
conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, pilot_id) VALUES (2, 'FL4321', 8, '2025-05-11 10:50', 2);")
conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, pilot_id) VALUES (3, 'FL2345', 2, '2025-05-11 08:30', 1);")
conn.execute("INSERT INTO flight (flight_id, flight_code, route_id, departure_time, pilot_id) VALUES (4, 'FL5432', 9, '2025-05-12 09:15', 1);")

# Calculate arrival times for all flights using the duration_minutes from route
conn.execute("UPDATE flight SET arrival_time = DATETIME(departure_time, '+' || (SELECT duration_minutes FROM route WHERE flight.route_id = route.route_id) || ' minute') WHERE 1=1")

# Commit the changes to the database
conn.commit()

# Messages to show end of seeding
print("Records created successfully")
print("Total number of rows created :", conn.total_changes)
print("\n");

# ---------------------------- Functions ---------------------------------------- #
# -------------------------- Menu Functions ------------------------------------- #

# Function to display the main menu
def show_main_menu():
    # Show main menu
    print("===============================") 
    print("Choose what you want work with:")
    print("1) Flights")
    print("2) Pilots")
    print("3) Destinations")
    print("4) Routes")
    print("5) Summaries")
    print("6) Exit")
    print("===============================")
    choice = input("Enter your option >> ")
    process_menu_choice(choice)

# Function to process what has been chosen from the main menu
def process_menu_choice(choice):
    if choice == "1":
        show_action_menu("flight")
    elif choice == "2":
        show_action_menu("pilot")
    elif choice == "3":
        show_action_menu("destination")
    elif choice == "4":
        show_action_menu("route") 
    elif choice == "5":
        show_summary_menu()                 
    elif choice == "6":
        exit()
    else:
        print("Input not recognised, try again")   
        show_main_menu() 

# Function to show the Summary Menu if selected from the Main Menu
def show_summary_menu():
    print("===============================") 
    print("Choose what you want to see:")
    print("1) Number of flights leaving today")
    print("2) Number of flights for a Pilot")
    print("3) Number of flights leaving from an Airport")
    print("4) Go back")
    print("===============================")     
    choice = input("Enter your option >> ")
    process_summary_menu_choice(choice)

# Function to process the choice from the Summary Menu
def process_summary_menu_choice(choice):
    if choice == "1":
        count = get_flight_count_for_date("departure_time", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        if int(count) > 0:
            print("There are "+str(count)+" flight(s) leaving today")
        else:
            print("No flights are leaving today")
        show_main_menu()        
    elif choice == "2":
        value = input("Enter the Pilot Name >> ")
        column = "flight.pilot_name"
        count = get_flight_count(column, value)
        if int(count) > 0:
            print("There are "+str(count)+" flight(s) for pilot "+ value)
        else:
            print("There are no flights for pilot "+ value)
        show_main_menu()          
    elif choice == "3":
        value = input("Enter the Aiport Code >> ")
        column = "dep.airport_code"
        count = get_flight_count(column, value)
        if count > 0:
            print("There are "+str(count)+" flight(s) leaving from "+ value)
        else:
            print("There are no flights leaving from "+ value)
        show_main_menu() 
    elif choice == "4":
        show_main_menu()   
    else:
        print("Input not recognised, try again")   
        show_summary_menu()         

# Function to show the Action Menu if selected from the Main Menu
def show_action_menu(object):
    print("===============================")
    print("Choose what you want to do:")
    print("1) View a " + object)
    print("2) Amend a " + object)
    print("3) Add a " + object)
    print("4) Delete a " + object)
    print("5) Go back")
    print("===============================")     
    choice = input("Enter your option >> ")
    process_action_choice(object, choice)

def process_action_choice(object, choice):
    if choice == "1":
        show_view_menu(object)
    elif choice == "2":
        show_amend_menu(object)
    elif choice == "3":
        process_add_menu(object)
    elif choice == "4":
        show_delete_menu(object)
    elif choice == "5":
        show_main_menu()    
    else:
        print("Input not recognised, try again")  
        show_action_menu(object)  

# Function to show the View Menu if selected from the Main Menu
def show_view_menu(object):
    print("===============================")
    print("What do you want to search with:")
    if object == "flight":
        print("1) Flight Code")
        print("2) Departure Airport Code")
        print("3) Arrival Airport Code")
        print("4) Pilot Name")
        print("5) Departure Date")
        print("6) Arrival Date")
        print("7) Go back")
        print("===============================")          
        choice = input("Enter your option >> ")
        process_view_menu(choice, object)
    elif object == "pilot":
        print("1) Pilot Name")
        print("2) Go back")
        print("===============================") 
        choice = input("Enter your option >> ")
        process_view_menu_pilot(choice, object)
    elif object == "destination":
        print("1) Airport Code")
        print("2) Country")
        print("3) Go back")
        print("===============================") 
        choice = input("Enter your option >> ")
        process_view_menu_destination(choice, object)
    elif object == "route":
        print("1) Departure Airport Code")
        print("2) Arrival Airport Code")
        print("3) Go back")
        print("===============================") 
        choice = input("Enter your option >> ")
        process_view_menu_route(choice, object)


def process_view_menu_destination(choice, object):
    if choice == "1":
        value = input("Enter the Airport Code >> ")
        column = "airport_code"
    elif choice == "2":
        value = input("Enter the Country >> ")
        column = "country"  
    elif choice == "3":
        show_action_menu(object)   
    else:
        print("Input not recognised, try again")
        show_view_menu(object)                           
    display_airport_list(column, value)
    show_main_menu()

def process_view_menu_route(choice, object):
    if choice == "1":
        value = input("Enter the Departure Airport Code >> ")
        column = "arr.airport_code"
    elif choice == "2":
        value = input("Enter the Arrival Airport Code >> ")
        column = "arr.airport_code"      
    elif choice == "3":
        show_action_menu(object)   
    else:
        print("Input not recognised, try again")
        show_view_menu(object)        
    display_route_list(column, value)
    show_main_menu()

def process_view_menu_pilot(choice, object):
    if choice == "1":
        value = input("Enter the Pilot Name >> ")
        column = "pilot_name"
    elif choice == "2":
        show_action_menu(object)   
    else:
        print("Input not recognised, try again")
        show_view_menu(object)                
    display_pilot_list(column, value)           
    show_main_menu()

def process_view_menu(choice, object):
    if choice == "1":
        value = input("Enter the Flight Code >> ")
        column = "flight.flight_code"
    elif choice == "2":
        value = input("Enter the Departure Airport Code >> ")
        column = "dep.airport_code"
    elif choice == "3":
        value = input("Enter the Arrival Airport Code >> ")    
        column = "arr.airport_code"
    elif choice == "4":
        value = input("Enter the Pilot Name >> ")
        column = "flight.pilot_name"        
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
            column = "flight.arrival_time"
    elif choice == "7":
        show_action_menu(object)    
    else:
        print("Input not recognised, try again")
        show_view_menu(object)  
    process_view_choice(column, value)     

def process_view_choice(column, value):
    if "time" in column:
        display_flight_data_for_date(column, value)
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
    print("Choose a flight to amend:")
    id = input("Enter the Flight ID >> ")
    if display_flight_data("flight_id", id):
        print("===============================")
        print("Choose an attribute to update:")
        print("1) Departure Time")
        print("2) Arrival Time")
        print("3) Flight Status")
        print("4) Pilot")
        print("5) Go back") 
        print("===============================")             
        choice = input("Enter your option >> ")
        process_amend_flight_menu(choice, id) 
    else: 
        show_main_menu()   

# Function to show the Amend Menu if selected from the Main Menu
def process_amend_flight_menu(choice, id):
    recalculate_arrival = "N"
    if choice == "1":
        value = input("Enter the Departure Time (format YYYY-MM-DD HH:MM) >> ")    
        column = "departure_time"
        if validate_date_input(value, "%Y-%m-%d %H:%M"):
            recalculate_arrival = input("Do you want the Arrival Time to be recalculated? Y/N >> ")
        else: 
            print("Input not recognised, try again")
            process_amend_flight_menu(choice, id)
    elif choice == "2":
        value = input("Enter the Arrival Time >> ")
        column = "arrival_time"
    elif choice == "3":
        value = input("Enter the Flight Status >> ")    
        column = "status"
    elif choice == "4":
        value = input("Enter the Pilot ID >> ")    
        column = "pilot_id"
    elif choice == "5":
        show_action_menu("flight")    
    else:
        print("Input not recognised, try again") 
        process_amend_flight_menu(choice, id) 
    update_flight(column, value, id)
    if recalculate_arrival == "Y": 
        update_arrival_time(id)
    display_flight_data("flight_id", id)    
    show_main_menu()  

def show_amend_route_menu():
    print("Choose a route to amend:")
    id = input("Enter the Route ID >> ")
    if display_route_list("route.route_id", id): 
        print("===============================") 
        print("What do you want to change?")   
        print("1) Duration")
        print("2) Go back")  
        print("===============================") 
        choice = input("Enter your option >> ")
        process_amend_route_menu(choice, id) 
    else:
        show_main_menu()                
      

def process_amend_route_menu(choice, id):
    if choice == "1":
        value = input("Enter the Duration >> ")    
        if validate_numeric_input(value):
            column = "duration_minutes"
        else: 
            print("Input not recognised, try again")
            show_amend_route_menu()     
    elif choice == "2":
        show_action_menu("route")    
    else:
        print("Input not recognised, try again") 
        show_amend_route_menu() 
    update_route(column, value, id) 
    display_route_list("route.route_id", id)  
    show_main_menu()  

def show_amend_destination_menu():
    print("Choose an airport to amend: ")
    id = input("Enter the Airport ID >> ")
    if display_airport_list("airport_id", id):
        print("===============================") 
        print("What do you want to change?")  
        print("1) Airport Name")
        print("2) Go back")  
        print("===============================") 
        choice = input("Enter your option >> ")
        process_amend_destination_menu(choice, id)    
    else:
        show_main_menu() 

def process_amend_destination_menu(choice, id):
    if choice == "1":
        value = input("Enter the Airport Name >> ")    
        column = "airport_name"
    elif choice == "2":
        show_action_menu("destination")    
    else:
        print("Input not recognised, try again") 
        show_amend_destination_menu() 
    update_airport(column, value, id) 
    display_airport_list("airport_id", id) 
    show_main_menu()  

def show_amend_pilot_menu():
    print("Choose a pilot to amend:")
    id = input("Enter the Pilot ID >> ")
    if display_pilot_list("pilot_id", id):
        print("===============================") 
        print("What do you want to change?")  
        print("1) First Name")
        print("2) Last Name")
        print("3) Date Hired")
        print("4) Go back")   
        choice = input("Enter your option >> ")
        process_amend_pilot_menu(choice, id)      
    else:
        print("Pilot not found")    
        show_main_menu() 

def process_amend_pilot_menu(choice, id):
    if choice == "1":
        value = input("Enter the First Name >> ")    
        column = "first_name"
    elif choice == "2":
        value = input("Enter the Last Name >> ")    
        column = "last_name" 
    elif choice == "3":
        value = input("Enter the Date Hired (format YYYY-MM-DD) >> ")
        if validate_date_input(value, "%Y-%m-%d"):
            column = "date_hired"
        else: 
            print("Input not recognised, try again")
            process_amend_pilot_menu(choice, id)    
    elif choice == "4":
        show_action_menu("pilot")    
    else:
        print("Input not recognised, try again")  
    update_pilot(column, value, id)  
    display_pilot_list("pilot_id", id)
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
        print("Input not recognised, try again")   
        show_main_menu()    

def add_flight():
    flight_code = input("Enter the Flight Code >> ")
    if validate_flight_exists(flight_code):
        print("Flight already exists, no action taken")
        show_main_menu()
    else:    
        route_not_valid = True
        attempts = 0
        while route_not_valid and attempts < 3:
            departure_airport = input("Enter the Departure Airport Code >> ")
            arrival_airport = input("Enter the Arrival Airport Code >> ")
            route_id = get_route_id(departure_airport, arrival_airport)
            if route_id == None:
                print("Route "+str(departure_airport)+" to "+str(arrival_airport)+" not found, try again")
                attempts = attempts+1
            else:
                route_not_valid = False    
        if attempts>=3:
            print("Too many incorrect inputs, return to main menu")
            show_main_menu()        
        departure_time = input("Enter the Departure Time (format YYYY-MM-DD HH:MM) >> ")
        if validate_date_input(departure_time, "%Y-%m-%d %H:%M"):
            add_pilot = input("Do you want to assign the pilot now? Y/N >> ")
            if add_pilot == "Y":
                pilot_id = input("Enter the Pilot ID >> ")
            else: 
                pilot_id = -1    
            id = insert_flight(flight_code, route_id, departure_time, pilot_id)
            display_flight_data("flight_id", id)
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
        id = insert_airport(airport_code, airport_name, country)
        display_airport_list("airport_id", id)
    show_main_menu()       

def add_route():
    airport_exists = False
    attempts = 0
    while not airport_exists and attempts < 3:
        departure_airport_code = input("Enter the Departure Airport Code >> ")
        airport_exists = validate_airport_input(departure_airport_code)    
        if not airport_exists:
            print(str(departure_airport_code) +" not found, try again")
            attempts = attempts + 1
        else:
            departure_airport_id = get_airport_id(departure_airport_code)
            airport_exists = True   
            attempts = 0 
    if attempts >= 3:
        print("Too many incorrect inputs, return to main menu")
        show_main_menu()  
    airport_exists = False    
    while not airport_exists and attempts < 3:
        arrival_airport_code = input("Enter the Arrival Airport Code >> ")
        airport_exists = validate_airport_input(arrival_airport_code)                
        if not airport_exists:
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
            id = insert_route(departure_airport_id, arrival_airport_id, duration_minutes)
            display_route_list("route_id", id)
        else:
            print("Invalid input, start again")
            add_route()  
    show_main_menu()        


def add_pilot():
    first_name = input("Enter the First Name >> ")
    last_name = input("Enter the Last Name >> ")
    date_hired = input("Enter the Hire Date (format YYYY-MM-DD) >> ")
    if validate_date_input(date_hired, "%Y-%m-%d"):
        id = insert_pilot(first_name, last_name, date_hired)
        display_pilot_list("pilot_id", id)
    else:
        print("Date not recognised, start again")   
        add_pilot()
    show_main_menu()

# Function to show the Delete Menu if selected from the Main Menu
def show_delete_menu(object):
    if object == "flight":
        print("Choose a flight to delete:")
        flight_id = input("Enter the Flight ID >> ")
        if validate_numeric_input(flight_id):
            delete_flight(flight_id)
            show_main_menu()
        else: 
            print("Input not recognised, try again")
            show_delete_menu(object)    
    else:    
        print("No currently available, no action taken")
        show_main_menu()

# -------------------------- Validation Functions ------------------------------------- #

# Validate that the value is a number
def validate_numeric_input(value):
    return value.isnumeric()

# Validate that the value is an existing airport
def validate_airport_input(airport_code):
    sql = "SELECT '1' AS [Found] FROM airport WHERE airport_code = ?;"
    param = (''+airport_code+'',)
    airport = conn.execute(sql, param);
    for row in airport:
        if row[0] == "1":
            return True
    return False   

# Validate that the two airports are part of an existing route
def validate_route_exists(departure_airport_id, arrival_airport_id):
    sql = "SELECT '1' AS [Found] FROM route WHERE departure_airport_id = ? AND arrival_airport_id = ?;"
    param = (''+str(departure_airport_id)+'', ''+str(arrival_airport_id)+'',)
    route = conn.execute(sql, param)
    for row in route:
        if row[0] == "1":
            return True
    return False

# Validate that the value is an existing flight
def validate_flight_exists(flight_code):
    sql = "SELECT '1' AS [Found] FROM flight WHERE flight_code = ?;"
    param = (''+flight_code+'',)
    flight = conn.execute(sql, param)
    for row in flight:
        if row[0] == "1":
            return True
    return False

# Validate that the value is a date
def validate_date_input(date, format):
    valid = True
    try:
        valid = bool(datetime.strptime(date, format))
    except ValueError:
        valid = False
    return valid    

# ---------------------------- Transformations ------------------------------------- #   

def calculate_arrival_time(departure_time, duration):
    split_date = re.split('[- :]', departure_time)
    date_and_time = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), int(split_date[3]), int(split_date[4]), 0)
    time_change = timedelta(minutes=duration) 
    arrival_time = date_and_time + time_change 
    return arrival_time

def convert_to_table(data):
    table = tabulate(data, headers = "keys", tablefmt = "pipe")
    return table

def exit():
    print("Goodbye")

# -------------------------- SQL DML Functions ------------------------------------- #

# ------------------------------- Update ------------------------------------------- #

def update_pilot(column, value, id):
    sql = "UPDATE pilot SET "+column+" = ? WHERE pilot_id = " + id +";"
    param = (''+str(value)+'',)    
    pilot = conn.execute(sql, param)
    conn.commit()
    print(str(pilot.rowcount) + " pilot(s) updated") 

def update_flight(column, value, id):
    sql = "UPDATE flight SET "+column+" = ? where flight_id = "+ id +";"
    param = (''+str(value)+'',)   
    flight = conn.execute(sql, param)    
    conn.commit()
    print(str(flight.rowcount) + " flight(s) updated") 

def update_arrival_time(flight_id):
    sql = "UPDATE flight SET arrival_time = DATETIME(departure_time, '+' || (SELECT duration_minutes FROM route WHERE flight.route_id = route.route_id) || ' minute') WHERE flight_id = ?;"  
    param = (''+str(flight_id)+'',) 
    flight = conn.execute(sql, param)         
    conn.commit()
    print(str(flight.rowcount) +" arrival time(s) updated") 

def update_route(column, value, id):
    sql = "UPDATE route SET "+column+" = ? where route_id = "+ id +";"
    param = (''+str(value)+'',) 
    route = conn.execute(sql, param)   
    conn.commit()
    print(str(route.rowcount) + " route(s) updated")     

def update_airport(column, value, id):
    sql = "UPDATE airport SET "+column+" = ? where airport_id = "+ id +";"
    param = (''+str(value)+'',) 
    airport = conn.execute(sql, param)   
    conn.commit()
    print(str(airport.rowcount) + " destination(s) updated")        

# ------------------------------- Insert ------------------------------------------- #

def insert_flight(flight_code, route_id, departure_time, pilot_id):
    duration_minutes = get_duration_minutes(route_id)
    arrival_time = calculate_arrival_time(departure_time, duration_minutes)
    param = (''+str(flight_code)+'',''+str(route_id)+'',''+str(departure_time)+'',''+str(arrival_time)+'',''+str(pilot_id)+'',''+str(pilot_id)+'',) 
    sql = "INSERT INTO flight (flight_id, flight_code, route_id, departure_time, arrival_time, pilot_id) \
           VALUES (NULL, ?, ?, ?, ?, CASE ? WHEN '-1' THEN NULL ELSE ? END);"
    flight = conn.execute(sql, param)
    conn.commit()
    print(str(flight.rowcount) + " flight(s) inserted")
    return flight.lastrowid

def insert_airport(airport_code, airport_name, country):
    sql = "INSERT INTO airport (airport_id, airport_code, airport_name, country) VALUES (NULL, ?, ?, ?);"
    param = (''+str(airport_code)+'',''+str(airport_name)+'',''+str(country)+'',)   
    airport = conn.execute(sql, param)
    conn.commit()
    print(str(airport.rowcount) + " destinations(s) inserted")
    return airport.lastrowid

def insert_pilot(first_name, last_name, date_hired):
    sql = "INSERT INTO pilot (pilot_id, first_name, last_name, date_hired) VALUES (NULL, ?, ?, ?);"
    param = (''+str(first_name)+'', ''+str(last_name)+'', ''+str(date_hired)+'',) 
    pilot = conn.execute(sql, param)
    conn.commit()
    print(str(pilot.rowcount) +" pilot(s) inserted")
    return pilot.lastrowid

def insert_route(departure_airport_id, arrival_airport_id, duration_minutes):
    sql = "INSERT INTO route (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (null, ?, ?, ?);"
    param = (''+str(departure_airport_id)+'', ''+str(arrival_airport_id)+'', ''+str(duration_minutes)+'', ) 
    route = conn.execute(sql, param)
    conn.commit()
    print(str(route.rowcount) + " route(s) inserted")
    return route.lastrowid  

# ------------------------------- Select ------------------------------------------- #

# Function to get the route_id from route for a given pair of airports. If route does not exist, None is returned
def get_route_id(departure_airport_code, arrival_airport_code):
    sql = "SELECT route_id FROM route, airport AS dep, airport AS arr \
                         WHERE route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id \
                         AND dep.airport_code = ? AND arr.airport_code = ?;"
    param = (''+str(departure_airport_code)+'', ''+str(arrival_airport_code)+'',)   
    route = conn.execute(sql, param)
    for row in route:
        return row[0]
    return None

# Function to get the flight duration for a given route_id. If route does not exist, None is returned
def get_duration_minutes(route_id):
    route = conn.execute("SELECT duration_minutes FROM route WHERE route_id = '"+str(route_id)+"';")
    for row in route:
        return row[0]
    return None        

# Function to get the airport_id for a given airport_code. If airport does not exist, None is returned
def get_airport_id(airport_code):
    sql = "SELECT airport_id FROM airport WHERE airport_code = ?;"
    param = (''+str(airport_code)+'',) 
    airport = conn.execute(sql, param)  
    for row in airport:
        return row[0]
    return None

# Function to get the count of flights for a given predicate which is a string or number. If no flights meet the search criteria, 0 is returned
def get_flight_count(column, value):
    sql = "SELECT COUNT(*) AS [Count] \
                          FROM flight_and_pilot AS flight, route, airport AS dep, airport AS arr \
                          WHERE route.route_id = flight.route_id \
                          AND route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id \
                          AND "+str(column)+" = ?;"
    param = (''+str(value)+'',)
    flight = conn.execute(sql, param) 
    for row in flight:
        return int(row[0])
    return 0

# Function to get the count of flights for a given predicate which is a date. If no flights meet the search criteria, 0 is returned
def get_flight_count_for_date(column, date_value):
    split_date = re.split('[- :]', date_value)
    start_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    add_day = timedelta(days=1)
    end_date = start_date+add_day
    sql = "SELECT COUNT(*) AS Count \
                          FROM flight_and_pilot AS flight, route, airport AS source, airport AS dest \
                          WHERE route.route_id = flight.route_id \
                          AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id \
                          AND "+str(column)+" BETWEEN ? AND ?;"
    param = (''+str(start_date)+'', ''+str(end_date)+'',)
    flight = conn.execute(sql, param)   
    for row in flight:
        return int(row[0])
    return 0

# Function to get the routes for a given predicate. If no routes meet the search criteria, "No results found" is displayed to the user
def display_route_list(column, value):
    sql = "SELECT route_id AS [Route ID], dep.airport_code AS [Departure Airport Code], dep.airport_name AS [Departure Airport], arr.airport_code AS [Arrival Airport Code], arr.airport_name AS [Arrival Airport], duration_minutes AS [Duration] FROM route, airport AS dep, airport AS arr \
                         WHERE route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id AND "+column+" = ?;"
    param = (''+str(value)+'',)
    route = conn.execute(sql, param)  
    table = convert_to_table(route)
    if not table:
        print("No results found")
        return False
    else:    
        print(table)
        return True 

# Function to get the pilots for a given predicate. If no pilots meet the search criteria, "No results found" is displayed to the user
def display_pilot_list(column, value):
    sql = "SELECT pilot_id AS [Pilot ID], pilot_name AS [Pilot Name], date_hired AS [Date Hired] FROM pilot WHERE "+column+" = ?;"
    param = (''+str(value)+'',)  
    pilot = conn.execute(sql, param)  
    table = convert_to_table(pilot)
    if not table:
        print("No results found")
        return False
    else:    
        print(table)
        return True

# Function to get the airports for a given predicate. If no airports meet the search criteria, "No results found" is displayed to the user
def display_airport_list(column, value):
    sql = "SELECT airport_id AS [Airport ID], airport_name AS [Airport Name], airport_code AS [Airport Code], country AS [Country] \
        FROM airport WHERE "+column+" = ?;"
    param = (''+str(value)+'',)
    airport = conn.execute(sql, param) 
    table = convert_to_table(airport)
    if not table:
        print("No results found")
        return False
    else:    
        print(table)   
        return True

# Function to get the flights using a datetime attribute in its predicate. If no flights meet the search criteria, "No results found" is displayed to the user
def display_flight_data_for_date(column, date_value):
    split_date = re.split('[- :]', date_value)
    start_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    add_day = timedelta(days = 1)
    end_date = start_date + add_day
    sql = "SELECT flight_id AS [Flight ID], flight_code AS [Flight Code], source.airport_name AS [Departure Airport], dest.airport_name AS [Arrival Airport], \
                          departure_time AS [Departure Time], arrival_time AS [Arrival Time], pilot_name AS [Pilot Name], status AS [Status] \
                          FROM flight_and_pilot AS flight, route, airport AS source, airport AS dest \
                          WHERE route.route_id = flight.route_id \
                          AND route.departure_airport_id = source.airport_id AND route.arrival_airport_id = dest.airport_id \
                          AND "+str(column)+" BETWEEN ? AND ?;"
    param = (''+str(start_date)+'', ''+str(end_date)+'',)
    flight = conn.execute(sql, param)    
    table = convert_to_table(flight)
    if not table:
        print("No results found")
        return False
    else:    
        print(table)   
        return True

# Function to get the flights using a non-date attribute in its predicate. If no flights meet the search criteria, "No results found" is displayed to the user
def display_flight_data(column, value):
    sql = "SELECT flight_id AS [Flight ID], flight_code AS [Flight Code], dep.airport_name AS [Departure Airport], arr.airport_name AS [Arrival Airport], \
                          departure_time AS [Departure Time], arrival_time AS [Arrival Time], pilot_name AS [Pilot Name], status AS [Status] \
                          FROM flight_and_pilot AS flight, route, airport AS dep, airport AS arr \
                          WHERE route.route_id = flight.route_id \
                          AND route.departure_airport_id = dep.airport_id AND route.arrival_airport_id = arr.airport_id \
                          AND "+str(column)+" = ?;"
    param = (''+str(value)+'',)
    flight = conn.execute(sql, param)                       
    print("===============================")
    table = convert_to_table(flight)
    if not table:
        print("No results found")
        return False
    else:    
        print(table)
        return True


# ---------------------Delete ------------------------#

def delete_flight(flight_id):
    sql = "DELETE FROM flight WHERE flight_id = ?;"
    param = (''+str(flight_id)+'',)
    flight = conn.execute(sql,param)
    conn.commit()
    print(str(flight.rowcount) +" flight(s) deleted")

# -------------------------- Start of UI application ------------------------------------- #

show_main_menu()

