from datetime import datetime, timedelta, date
import re 
import sqlite3
from tabulate import tabulate

# --------------------------- Database set up ------------------------------ #
conn = sqlite3.connect('flight_management')
print ("Database has been created")

# Drop tables and views if they already exist in the database
conn.execute("DROP TABLE IF EXISTS flights;")
conn.execute("DROP TABLE IF EXISTS pilots;")
conn.execute("DROP TABLE IF EXISTS airports;")
conn.execute("DROP TABLE IF EXISTS routes;")
conn.execute("DROP TABLE IF EXISTS status;")
conn.execute("DROP VIEW IF EXISTS flights_and_pilots;")

# Create tables in the database
conn.execute("CREATE TABLE airports (airport_id INTEGER PRIMARY KEY NOT NULL, airport_name VARCHAR(50) NOT NULL, airport_code VARCHAR(3) NOT NULL, country VARCHAR(50) NOT NULL)")
conn.execute("CREATE TABLE pilots (pilot_id INTEGER PRIMARY KEY NOT NULL, first_name VARCHAR(50) NOT NULL, last_name VARCHAR(50) NOT NULL, pilot_name VARCHAR(100) GENERATED ALWAYS AS (first_name || ' ' || last_name) VIRTUAL NOT NULL, date_hired DATE NULL)")
conn.execute("CREATE TABLE routes (route_id INTEGER PRIMARY KEY NOT NULL, departure_airport_id INTEGER REFERENCES airport(airport_id) NOT NULL, arrival_airport_id INTEGER REFERENCES airport(airport_id) NOT NULL, duration_minutes INTEGER NOT NULL)")
conn.execute("CREATE TABLE status (status_id INTEGER PRIMARY KEY NOT NULL, status_name VARCHAR(10) NOT NULL, description VARCHAR(50) NOT NULL)")
conn.execute("CREATE TABLE flights (flight_id INTEGER PRIMARY KEY NOT NULL, flight_code VARCHAR(10) NOT NULL, route_id INTEGER REFERENCES route(route_id) NOT NULL, departure_time DATETIME NOT NULL, arrival_time DATETIME NULL, pilot_id INTEGER REFERENCES pilot(pilot_id) NULL, status_id VARCHAR(15) DEFAULT 1 NULL);")

# Create views in the database
conn.execute("CREATE VIEW flights_and_pilots AS SELECT flight_id, flight_code, route_id, departure_time, arrival_time, IFNULL(pilots.pilot_id, 'Unassigned') AS [pilot_id], IFNULL(pilot_name, 'Unassigned') AS [pilot_name], date_hired, status.status_id, status.status_name FROM flights, status LEFT JOIN pilots ON flights.pilot_id = pilots.pilot_id WHERE flights.status_id = status.status_id")

# Insert seeding data to pilots table
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (1, 'Joseph','Walters','2015-06-17');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (2, 'Jo','Walters','2022-05-31');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (3, 'Alan','Thomson','2007-12-17');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (4, 'Ian','Jackson','2022-04-14');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (5, 'Samantha','North','2013-07-19');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (6, 'Austin','Redman','2024-11-27');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (7, 'Bruce','Crowther','2007-06-16');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (8, 'Peter','Newman','2017-09-19');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (9, 'George','Langford','2022-05-03');")
conn.execute("INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (10, 'Nina','Palmer','2016-05-14');")

# Insert seeding data to airports table
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (1, 'London Gatwick', 'LGW', 'UK');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (2, 'London Luton', 'LTN', 'UK');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (3, 'London Heathrow', 'LHR', 'UK');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (4, 'Split', 'SPU', 'Croatia');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (5, 'Corfu', 'CFU', 'Greece');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (6, 'Pula', 'PUY', 'Croatia');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (7, 'Paris Orly', 'ORY', 'France');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (8, 'Berlin Brandenburg', 'BER', 'Germany');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (9, 'Brussels', 'BRU', 'Belgium');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (10, 'New York John F Kennedy Intl', 'JFK', 'USA');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (11, 'New York Newark Liberty Intl', 'EWR', 'USA');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (12, 'Lisbon', 'LIS', 'Portugal');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (13, 'Milan Bergamo/Orio al Serio', 'BGY', 'Italy');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (14, 'Rome Griffiss Intl', 'RME', 'Italy');")
conn.execute("INSERT INTO airports (airport_id, airport_name, airport_code, country) VALUES (15, 'Malaga Airport', 'AGP', 'Spain');")

# Insert seeding data to routes table
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (1, 1, 4, 139);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (2, 1, 5, 178);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (3, 1, 6, 121);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (4, 1, 7, 52);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (5, 1, 8, 100);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (6, 1, 9, 52);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (7, 1, 10, 443);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (8, 4, 1, 139);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (9, 5, 1, 178);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (10, 6, 1, 121);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (11, 7, 1, 52);")
conn.execute("INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (12, 8, 1, 100);")

# Insert seeding data to status table
conn.execute("INSERT INTO status (status_id, status_name, description) VALUES (1, 'Scheduled', 'Flight is scheduled');")
conn.execute("INSERT INTO status (status_id, status_name, description) VALUES (2, 'On Time', 'Flight is scheduled and is running on time');")
conn.execute("INSERT INTO status (status_id, status_name, description) VALUES (3, 'Boarding', 'Flight is boarding');")
conn.execute("INSERT INTO status (status_id, status_name, description) VALUES (4, 'Late', 'Flight is running late');")
conn.execute("INSERT INTO status (status_id, status_name, description) VALUES (5, 'Departed', 'Flight is in the air');")
conn.execute("INSERT INTO status (status_id, status_name, description) VALUES (6, 'Landed', 'Flight has landed');")
conn.execute("INSERT INTO status (status_id, status_name, description) VALUES (7, 'Complete', 'Flight has landed and is complete');")

# Insert seeding data to flights table
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id, status_id) VALUES (1, 'FL1234', 1, '2025-04-01 07:10', 1, 5);")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id, status_id) VALUES (2, 'FL4321', 8, '2025-04-01 10:50', 2, 4);")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id, status_id) VALUES (3, 'FL2345', 2, '2025-04-02 08:30', 3, 4);")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id, status_id) VALUES (4, 'FL5432', 9, '2025-04-02 09:15', 4, 6);")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id) VALUES (5, 'FL3456', 3, '2025-05-12 09:15', 1);")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id) VALUES (6, 'FL6543', 10, '2025-05-13 09:15', 1);")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id) VALUES (7, 'FL4567', 4, '2025-05-14 09:15', 1);")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id) VALUES (8, 'FL7654', 11, '2025-05-15 09:15', 1);")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time) VALUES (9, 'FL5678', 5, '2025-05-16 09:15');")
conn.execute("INSERT INTO flights (flight_id, flight_code, route_id, departure_time) VALUES (10, 'FL8765', 12, '2025-05-17 09:15');")

# Calculate arrival times for all flights using the duration_minutes from routes
conn.execute("UPDATE flights SET arrival_time = DATETIME(departure_time, '+' || (SELECT duration_minutes FROM routes WHERE flights.route_id = routes.route_id) || ' minute') WHERE 1=1")

# Commit the changes to the database
conn.commit()

# Messages to show end of seeding
print("Records created successfully")
print("Total number of rows created :", conn.total_changes)
print("\n");

# ------------------------------ Functions --------------------------------- #
# ---------------------------- Menu Functions ------------------------------ #

def show_main_menu():
    """Display the main menu"""
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

def process_menu_choice(choice):
    """Process what has been chosen from the main menu"""
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

def show_summary_menu():
    """Display the Summary Menu"""
    print("===============================") 
    print("Choose what you want to see:")
    print("1) Number of flights leaving today")
    print("2) Number of flights for a Pilot")
    print("3) Number of flights leaving from an Airport")
    print("4) Go back")
    print("===============================")     
    choice = input("Enter your option >> ")
    process_summary_menu_choice(choice)

def process_summary_menu_choice(choice):
    """Process what has been chosen from the Summary Menu"""
    if choice == "1":
        count = get_flight_count_for_date("departure_time", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        if int(count) > 0:
            print("There are "+str(count)+" flight(s) leaving today")
        else:
            print("No flights are leaving today")
        show_main_menu()        
    elif choice == "2":
        value = input("Enter the Pilot Name >> ")
        column = "flights.pilot_name"
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

def show_action_menu(entity):
    """Display the Action Menu"""
    print("===============================")
    print("Choose what you want to do:")
    print("1) View a " + entity)
    print("2) Amend a " + entity)
    print("3) Add a " + entity)
    print("4) Delete a " + entity)
    print("5) Go back")
    print("===============================")     
    choice = input("Enter your option >> ")
    process_action_choice(entity, choice)

def process_action_choice(entity, choice):
    """Process what has been chosen from the Action Menu"""
    if choice == "1":
        show_view_menu(entity)
    elif choice == "2":
        show_amend_menu(entity)
    elif choice == "3":
        process_add_menu(entity)
    elif choice == "4":
        show_delete_menu(entity)
    elif choice == "5":
        show_main_menu()    
    else:
        print("Input not recognised, try again")  
        show_action_menu(entity)  

def show_view_menu(entity):
    """Display View Menu"""
    print("===============================")
    print("What do you want to search with:")
    # Different options depending on the entity chosen
    if entity == "flight":
        print("1) Flight Code")
        print("2) Departure Airport Code")
        print("3) Arrival Airport Code")
        print("4) Pilot Name")
        print("5) Departure Date")
        print("6) Arrival Date")
        print("7) Go back")
        print("===============================")          
        choice = input("Enter your option >> ")
        process_view_menu_flight(choice, entity)
    elif entity == "pilot":
        print("1) Pilot Name")
        print("2) Go back")
        print("===============================") 
        choice = input("Enter your option >> ")
        process_view_menu_pilot(choice, entity)
    elif entity == "destination":
        print("1) Airport Code")
        print("2) Country")
        print("3) Go back")
        print("===============================") 
        choice = input("Enter your option >> ")
        process_view_menu_destination(choice, entity)
    elif entity == "route":
        print("1) Departure Airport Code")
        print("2) Arrival Airport Code")
        print("3) Go back")
        print("===============================") 
        choice = input("Enter your option >> ")
        process_view_menu_route(choice, entity)
    else: 
        show_main_menu()    

def process_view_menu_destination(choice, entity):
    """Process what has been chosen from the View Menu when entity selected was destination"""
    if choice == "1":
        value = input("Enter the Airport Code >> ")
        column = "airport_code"
    elif choice == "2":
        value = input("Enter the Country >> ")
        column = "country"  
    elif choice == "3":
        show_action_menu(entity)   
    else:
        print("Input not recognised, try again")
        show_view_menu(entity)                           
    display_airport_list(column, value)
    show_main_menu()

def process_view_menu_route(choice, entity):
    """Process what has been chosen from the View Menu when entity selected was route"""
    if choice == "1":
        value = input("Enter the Departure Airport Code >> ")
        column = "dep.airport_code"
    elif choice == "2":
        value = input("Enter the Arrival Airport Code >> ")
        column = "arr.airport_code"      
    elif choice == "3":
        show_action_menu(entity)   
    else:
        print("Input not recognised, try again")
        show_view_menu(entity)        
    display_route_list(column, value)
    show_main_menu()

def process_view_menu_pilot(choice, entity):
    """Process what has been chosen from the View Menu when entity selected was pilot"""
    if choice == "1":
        value = input("Enter the Pilot Name >> ")
        column = "pilot_name"
    elif choice == "2":
        show_action_menu(entity)   
    else:
        print("Input not recognised, try again")
        show_view_menu(entity)                
    display_pilot_list(column, value) 
    view_schedule = input("Do you want to view this pilot's schedule? (Y/N) >> ")
    if (view_schedule == "Y"):
        display_flight_list(column, value)  
    show_main_menu()

def process_view_menu_flight(choice, entity):
    """Process what has been chosen from the View Menu when entity selected was flight"""
    if choice == "1":
        value = input("Enter the Flight Code >> ")
        column = "flights.flight_code"
    elif choice == "2":
        value = input("Enter the Departure Airport Code >> ")
        column = "dep.airport_code"
    elif choice == "3":
        value = input("Enter the Arrival Airport Code >> ")    
        column = "arr.airport_code"
    elif choice == "4":
        value = input("Enter the Pilot Name >> ")
        column = "flights.pilot_name"        
    elif choice == "5":
        value = input("Enter the Departure Day (format YYYY-MM-DD) >> ")
        if not validate_date_input(value, "%Y-%m-%d"):
            print("Input not recognised, try again")
            process_view_menu_flight(choice, entity)
        else:
            column = "flights.departure_time"
    elif choice == "6":
        value = input("Enter the Arrival Day (format YYYY-MM-DD) >> ")
        if not validate_date_input(value, "%Y-%m-%d"):
            print("Input not recognised, try again")
            process_view_menu_flight(choice, entity)
        else:
            column = "flights.arrival_time"
    elif choice == "7":
        show_action_menu(entity)    
    else:
        print("Input not recognised, try again")
        show_view_menu(entity)  
    process_view_choice(column, value)     

# 
def process_view_choice(column, value):
    """Process what has been chosen from the View Flight Menu"""
    if "time" in column:
        display_flight_list_for_date(column, value)
    else:
        display_flight_list(column, value)
    show_main_menu()

def show_amend_menu(entity):
    """Direct to the correct Amend Menu for the entity chosen"""
    if entity == "flight":
        show_amend_flight_menu()
    if entity == "route":
        show_amend_route_menu()  
    if entity == "destination":
        show_amend_destination_menu()     
    if entity == "pilot":
        show_amend_pilot_menu()                 

def show_amend_flight_menu():
    """Display the Amend Flight Menu"""
    print("Choose a flight to amend:")
    id = input("Enter the Flight ID >> ")
    if display_flight_list("flight_id", id):
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

def process_amend_flight_menu(choice, id):
    """Process the input from the Amend Flight Menu and guide user through options"""
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
        if(get_status_id(value) > 0):
            value = get_status_id(value)
            column = "status_id"
        else:
            print("Status not recognised, try again") 
            process_amend_flight_menu(choice, id)    
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
    display_flight_list("flight_id", id)    
    show_main_menu()  

def show_amend_route_menu():
    """Display the Amend Route Menu"""
    print("Choose a route to amend:")
    id = input("Enter the Route ID >> ")
    if display_route_list("routes.route_id", id): 
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
    """Process the input from the Amend Route Menu and guide user through options"""
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
    display_route_list("routes.route_id", id)  
    show_main_menu()  

def show_amend_destination_menu():
    """Display the Amend Destination Menu"""
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
    """Process the input from the Amend Destination Menu and guide user through options"""
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
    """Display the Amend Pilot Menu"""
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
    """Process the input from the Amend Pilot Menu and guide user through options"""
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

def process_add_menu(entity):
    """Direct the user to the correct Add Menu for the entity chosen"""
    if entity == "flight":
        show_add_flight_menu()
    elif entity == "destination":
        show_add_airport_menu()
    elif entity == "route":
        show_add_route_menu()
    elif entity == "pilot":
        show_add_pilot_menu()        
    else:
        print("Input not recognised, try again")   
        show_main_menu()    

def show_add_flight_menu():
    """Display the Add Flight Menu"""
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
            if route_id == -1:
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
            display_flight_list("flight_id", id)
            show_main_menu()   
        else: 
            print("Input not recognised, start again")
            show_add_flight_menu()
    show_main_menu()               

def show_add_airport_menu():
    """Display the Add Destination Menu"""
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

def show_add_route_menu():
    """Display the Add Route Menu"""
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
            show_add_route_menu()  
    show_main_menu()        

def show_add_pilot_menu():
    """Display the Add Pilot Menu"""
    first_name = input("Enter the First Name >> ")
    last_name = input("Enter the Last Name >> ")
    date_hired = input("Enter the Hire Date (format YYYY-MM-DD) >> ")
    if validate_date_input(date_hired, "%Y-%m-%d"):
        id = insert_pilot(first_name, last_name, date_hired)
        display_pilot_list("pilot_id", id)
    else:
        print("Date not recognised, start again")   
        show_add_pilot_menu()
    show_main_menu()

def show_delete_menu(entity):
    """Display the Delete Menu"""
    if entity == "flight":
        print("Choose a flight to delete:")
        flight_id = input("Enter the Flight ID >> ")
        if validate_numeric_input(flight_id):
            delete_flight(flight_id)
            show_main_menu()
        else: 
            print("Input not recognised, try again")
            show_delete_menu(entity)    
    else:    
        print("No currently available, no action taken")
        show_main_menu()

# ---------------------- Validation Functions ------------------------------ #

def validate_numeric_input(value):
    """Validate that the value is a number"""
    return value.isnumeric()

def validate_airport_input(airport_code):
    """Validate that the value is an existing airport"""
    # SELECT query to return '1' if there exists a row in the airports table with the airport_code value
    sql = "SELECT '1' AS [Found] FROM airports WHERE airport_code = ?;"
    param = (''+airport_code+'',)
    airport = conn.execute(sql, param);
    return return_row_exists(airport)       

def validate_route_exists(departure_airport_id, arrival_airport_id):
    """Validate that the two airports are part of an existing route"""
    # SELECT query to return '1' if there exists a row in the routes table with the departure_airport_id and arrival_airport_id value
    sql = "SELECT '1' AS [Found] FROM routes WHERE departure_airport_id = ? AND arrival_airport_id = ?;"
    param = (''+str(departure_airport_id)+'', ''+str(arrival_airport_id)+'',)
    route = conn.execute(sql, param)
    return return_row_exists(route)    

def validate_flight_exists(flight_code):
    """Validate that the value is an existing flight"""
    # SELECT query to return '1' if there exists a row in the flights table with the flight_code value
    sql = "SELECT '1' AS [Found] FROM flights WHERE flight_code = ?;"
    param = (''+flight_code+'',)
    flight = conn.execute(sql, param)
    return return_row_exists(flight)

def validate_date_input(date, format):
    """Validate that the value is a date"""
    valid = True
    try:
        valid = bool(datetime.strptime(date, format))
    except ValueError:
        valid = False
    return valid    

# --------------------------- Common Functions ----------------------------- #   

def convert_to_table(data):
    """Format data from the database into a user-friendly table"""
    table = tabulate(data, headers = "keys", tablefmt = "pipe")
    return table

def return_data(data):
    """Check if results are found, and if so, print them"""
    table = convert_to_table(data)
    if not table:
        print("No results found")
        return False
    else:    
        print(table)   
        return True

def return_row_exists(data):
    """Check if results are found, and return a boolean of True (found) or False (not found)"""
    for row in data:
        if row[0] == "1":
            return True
    return False 

def exit():
    """Exit the application"""
    print("Goodbye")

# -------------------------- SQL DML Functions ----------------------------- #
# ------------------------------ UPDATE ------------------------------------ #

def update_pilot(column, value, id):
    """Update a row in the pilots table to change an attribute to a new value"""
    # UPDATE query to change the value of an attribute for the pilot_id requested in the pilots table
    sql = "UPDATE pilots SET "+str(column)+" = ? WHERE pilot_id = " + id +";"
    param = (''+str(value)+'',)    
    pilot = conn.execute(sql, param)
    conn.commit()
    print(str(pilot.rowcount) + " pilot(s) updated") 

def update_flight(column, value, id):
    """Update a row in the flights table to change an attribute to a new value"""
    # UPDATE query to change the value of an attribute for the flight_id requested in the flights table
    sql = "UPDATE flights SET "+str(column)+" = ? where flight_id = "+ id +";"
    param = (''+str(value)+'',)   
    flight = conn.execute(sql, param)    
    conn.commit()
    print(str(flight.rowcount) + " flight(s) updated") 

def update_arrival_time(flight_id):
    """Update a row in the flights table to calculate a new value of arrival_time based on duration_minutes from routes table"""
    # UPDATE query to calculate and change the arrival_time for the flight_id requested in the flights table    
    sql = "UPDATE flights SET arrival_time = DATETIME(departure_time, '+' || (SELECT duration_minutes FROM routes \
        WHERE flights.route_id = routes.route_id) || ' minute') WHERE flight_id = ?;"  
    param = (''+str(flight_id)+'',) 
    flight = conn.execute(sql, param)         
    conn.commit()
    print(str(flight.rowcount) +" arrival time(s) updated") 

def update_route(column, value, id):
    """Update a row in the routes table to change an attribute to a new value"""
    # UPDATE query to change the value of an attribute for the route_id requested in the routes table    
    sql = "UPDATE routes SET "+str(column)+" = ? where route_id = "+ id +";"
    param = (''+str(value)+'',) 
    route = conn.execute(sql, param)   
    conn.commit()
    print(str(route.rowcount) + " route(s) updated")     

def update_airport(column, value, id):
    """Update a row in the airports table to change an attribute to a new value"""
    # UPDATE query to change the value of an attribute for the airport_id requested in the airports table       
    sql = "UPDATE airports SET "+str(column)+" = ? where airport_id = "+ id +";"
    param = (''+str(value)+'',) 
    airport = conn.execute(sql, param)   
    conn.commit()
    print(str(airport.rowcount) + " destination(s) updated")        

# ------------------------------ INSERT ------------------------------------ #

def insert_flight(flight_code, route_id, departure_time, pilot_id):
    """Insert a new row into flights table"""
    # INSERT query to add a row to the flights table with the values provided   
    sql = "INSERT INTO flights (flight_id, flight_code, route_id, departure_time, pilot_id) \
           VALUES (NULL, ?, ?, ?, CASE ? WHEN '-1' THEN NULL ELSE ? END);"
    param = (''+str(flight_code)+'',''+str(route_id)+'',''+str(departure_time)+'',''+str(pilot_id)+'',''+str(pilot_id)+'',) 
    flight = conn.execute(sql, param)
    conn.commit()
    print(str(flight.rowcount) + " flight(s) inserted")
    # Calculate and update with arrival_time
    update_arrival_time(flight.lastrowid);
    return flight.lastrowid

def insert_airport(airport_code, airport_name, country):
    """Insert a new row into airports table"""
    # INSERT query to add a row to the airports table with the values provided       
    sql = "INSERT INTO airports (airport_id, airport_code, airport_name, country) VALUES (NULL, ?, ?, ?);"
    param = (''+str(airport_code)+'',''+str(airport_name)+'',''+str(country)+'',)   
    airport = conn.execute(sql, param)
    conn.commit()
    print(str(airport.rowcount) + " destinations(s) inserted")
    return airport.lastrowid

def insert_pilot(first_name, last_name, date_hired):
    """Insert a new row into pilots table"""
    # INSERT query to add a row to the pilots table with the values provided      
    sql = "INSERT INTO pilots (pilot_id, first_name, last_name, date_hired) VALUES (NULL, ?, ?, ?);"
    param = (''+str(first_name)+'', ''+str(last_name)+'', ''+str(date_hired)+'',) 
    pilot = conn.execute(sql, param)
    conn.commit()
    print(str(pilot.rowcount) +" pilot(s) inserted")
    return pilot.lastrowid

def insert_route(departure_airport_id, arrival_airport_id, duration_minutes):
    """Insert a new row into routes table"""
    # INSERT query to add a row to the routes table with the values provided       
    sql = "INSERT INTO routes (route_id, departure_airport_id, arrival_airport_id, duration_minutes) VALUES (NULL, ?, ?, ?);"
    param = (''+str(departure_airport_id)+'', ''+str(arrival_airport_id)+'', ''+str(duration_minutes)+'', ) 
    route = conn.execute(sql, param)
    conn.commit()
    print(str(route.rowcount) + " route(s) inserted")
    return route.lastrowid  

# ------------------------------ SELECT ------------------------------------ #

def get_status_id(status_name):
    """Get the status id for a given status_name. If status does not exist, -1 is returned"""
    # SELECT query to return the status_id from the status table for the provided status_name value    
    sql = "SELECT status_id FROM status WHERE status_name = ?;"
    param = (''+status_name+'',)
    status = conn.execute(sql, param)
    for row in status:
        return row[0]
    return -1  

def get_route_id(departure_airport_code, arrival_airport_code):
    """Get the route_id from route for a given pair of airports. If route does not exist, -1 is returned"""
    # SELECT query to return the route_id from the routes and airports tables for the provided departure_airport_code and arrival_airport_code value        
    sql = "SELECT route_id FROM routes, airports AS dep, airports AS arr \
                         WHERE routes.departure_airport_id = dep.airport_id AND routes.arrival_airport_id = arr.airport_id \
                         AND dep.airport_code = ? AND arr.airport_code = ?;"
    param = (''+str(departure_airport_code)+'', ''+str(arrival_airport_code)+'',)   
    route = conn.execute(sql, param)
    for row in route:
        return row[0]
    return -1  

def get_duration_minutes(route_id):
    """Get the flight duration for a given route_id. If route does not exist, -1 is returned"""
    # SELECT query to return the duration_minutes from the routes table for the provided route_id value     
    route = conn.execute("SELECT duration_minutes FROM routes WHERE route_id = '"+str(route_id)+"';")
    for row in route:
        return row[0]
    return -1     

def get_airport_id(airport_code):
    """Get the airport_id for a given airport_code. If airport does not exist, -1 is returned"""
    # SELECT query to return the airport_id from the airports table for the provided airport_code value      
    sql = "SELECT airport_id FROM airports WHERE airport_code = ?;"
    param = (''+str(airport_code)+'',) 
    airport = conn.execute(sql, param)  
    for row in airport:
        return row[0]
    return -1  

def get_flight_count(column, value):
    """Get the count of flights for a given value (which is a string or number) in a given column. If no flights meet the search criteria, 0 is returned"""
    # SELECT query to return the count of rows the flights_and_pilots view joined with routes and airports tables for the provided attribute value       
    sql = "SELECT COUNT(*) AS [Count] \
                          FROM flights_and_pilots AS flights, routes, airports AS dep, airports AS arr \
                          WHERE routes.route_id = flights.route_id \
                          AND routes.departure_airport_id = dep.airport_id AND routes.arrival_airport_id = arr.airport_id \
                          AND "+str(column)+" = ?;"
    param = (''+str(value)+'',)
    flight = conn.execute(sql, param) 
    for row in flight:
        return row[0]
    return 0  

def get_flight_count_for_date(column, date_value):
    """Get the count of flights for a given value (which is a date) in a given column. If no flights meet the search criteria, 0 is returned"""
    split_date = re.split('[- :]', date_value)
    start_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    add_day = timedelta(days=1)
    end_date = start_date+add_day
    # SELECT query to return the count of rows the flights_and_pilots view joined with routes and airports tables for the provided attribute date value      
    sql = "SELECT COUNT(*) AS [Count] \
                          FROM flights_and_pilots AS flights, routes, airports AS dep, airports AS arr \
                          WHERE routes.route_id = flights.route_id \
                          AND routes.departure_airport_id = dep.airport_id AND routes.arrival_airport_id = arr.airport_id \
                          AND "+str(column)+" BETWEEN ? AND ?;"
    param = (''+str(start_date)+'', ''+str(end_date)+'',)
    flight = conn.execute(sql, param)   
    for row in flight:
        return row[0]
    return 0  

def display_route_list(column, value):
    """Get the routes for a given value in a given column. If no routes meet the search criteria, "No results found" is displayed to the user"""
    # SELECT query to return multiple attributes for all rows in the routes and airports tables for the provided attribute value      
    sql = "SELECT route_id AS [Route ID], dep.airport_code AS [Departure Airport Code], dep.airport_name AS [Departure Airport], \
        arr.airport_code AS [Arrival Airport Code], arr.airport_name AS [Arrival Airport], duration_minutes AS [Duration] FROM routes, airports AS dep, airports AS arr \
        WHERE routes.departure_airport_id = dep.airport_id AND routes.arrival_airport_id = arr.airport_id AND "+str(column)+" = ?;"
    param = (''+str(value)+'',)
    route = conn.execute(sql, param)  
    return return_data(route)

def display_pilot_list(column, value):
    """Get the pilots for a given value in a given column. If no pilots meet the search criteria, "No results found" is displayed to the user"""
    # SELECT query to return multiple attributes for all rows in the pilots for the provided attribute value       
    sql = "SELECT pilot_id AS [Pilot ID], pilot_name AS [Pilot Name], date_hired AS [Date Hired] FROM pilots WHERE "+str(column)+" = ?;"
    param = (''+str(value)+'',)  
    pilot = conn.execute(sql, param)  
    return return_data(pilot)

def display_airport_list(column, value):
    """Get the airports for a given value in a given column. If no airports meet the search criteria, "No results found" is displayed to the user"""
    # SELECT query to return multiple attributes for all rows in the airports for the provided attribute value       
    sql = "SELECT airport_id AS [Airport ID], airport_name AS [Airport Name], airport_code AS [Airport Code], country AS [Country] \
        FROM airports WHERE "+str(column)+" = ?;"
    param = (''+str(value)+'',)
    airport = conn.execute(sql, param) 
    return return_data(airport)

def display_flight_list_for_date(column, date_value):
    """Get the flights for a given day (calculated from a datetime) in a given column. If no flights meet the search criteria, "No results found" is displayed to the user"""
    split_date = re.split('[- :]', date_value)
    start_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    add_day = timedelta(days = 1)
    end_date = start_date + add_day
    # SELECT query to return multiple attributes for all rows in the flights_and_pilots view joined with routes and airports tables for the provided attribute date value  
    sql = "SELECT flight_id AS [Flight ID], flight_code AS [Flight Code], dep.airport_name AS [Departure Airport], arr.airport_name AS [Arrival Airport], \
                          departure_time AS [Departure Time], arrival_time AS [Arrival Time], pilot_name AS [Pilot Name], status_name AS [Status] \
                          FROM flights_and_pilots AS flights, routes, airports AS dep, airports AS arr \
                          WHERE routes.route_id = flights.route_id \
                          AND routes.departure_airport_id = dep.airport_id AND routes.arrival_airport_id = arr.airport_id \
                          AND "+str(column)+" BETWEEN ? AND ?;"
    param = (''+str(start_date)+'', ''+str(end_date)+'',)
    flight = conn.execute(sql, param)    
    return return_data(flight)

def display_flight_list(column, value):
    """Get the flights using a non-date attribute in its predicate. If no flights meet the search criteria, "No results found" is displayed to the user"""
    # SELECT query to return multiple attributes for all rows in the flights_and_pilots view joined with routes and airports tables for the provided attribute value  
    sql = "SELECT flight_id AS [Flight ID], flight_code AS [Flight Code], dep.airport_name AS [Departure Airport], arr.airport_name AS [Arrival Airport], \
                          departure_time AS [Departure Time], arrival_time AS [Arrival Time], pilot_name AS [Pilot Name], status_name AS [Status] \
                          FROM flights_and_pilots AS flights, routes, airports AS dep, airports AS arr \
                          WHERE routes.route_id = flights.route_id \
                          AND routes.departure_airport_id = dep.airport_id AND routes.arrival_airport_id = arr.airport_id \
                          AND "+str(column)+" = ?;"
    param = (''+str(value)+'',)
    flight = conn.execute(sql, param)                       
    return return_data(flight)

# ------------------------------ DELETE ------------------------------------ #

def delete_flight(flight_id):
    """Delete a row from flights table using the flight_id"""
    # DELETE query to delete a row from the flights table with the provided flight_id value
    sql = "DELETE FROM flights WHERE flight_id = ?;"
    param = (''+str(flight_id)+'',)
    flight = conn.execute(sql,param)
    conn.commit()
    print(str(flight.rowcount) +" flight(s) deleted")

# --------------------- Start of UI application ---------------------------- #

show_main_menu()
