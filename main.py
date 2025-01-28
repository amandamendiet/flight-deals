#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from datetime import *
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
import time

# ----------------------------------- DEFINE FUNCTIONS ---------------------------------- #
def update_sheety_iata_codes():
    # for each city in the spreadsheet GET iata code and UPDATE it in the spreadsheet
    for city_info in sheety_data['prices']:
        iata_code = flight_search.search_cities_iata_code(city_info['city'])
        if city_info['iataCode'] != iata_code:
            city_info['iataCode'] = iata_code
            sheety_data_manager.update_city_iata_code(city_info['id'], city_info['iataCode'])


# ----------------------------------- SET UP THE FLIGHT SEARCH ---------------------------------- #
# create origin airport CONSTANT
DEPARTURE_IATA_CODE = "NYC"

# create objects
flight_search = FlightSearch()
sheety_data_manager = DataManager()
notification_manager = NotificationManager()

# get data from the spreadsheet
sheety_data_manager.get_sheet_data()
sheety_data = sheety_data_manager.sheety_destination_data

# create departure and return dates
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# ----------------------------------- UPDATE IATA CODES IN SHEETY ---------------------------------- #
# !!!! if sheety needs update call:
#update_sheety_iata_codes()

# ----------------------------------- GET YOUR USERS WHATSAPP NUMBERS ---------------------------------- #

user_data = sheety_data_manager.get_user_whatsapp_number()
# Verify the name of your email column in your sheet. Yours may be different from mine
user_whatsapp_list = [{row["whatIsYourFirstName?"]:row["whatIsYourWhatsappNumber?"]} for row in user_data]
print(f"Your Whatsapp list includes {user_whatsapp_list}")

# ----------------------------------- SEARCH THE CHEAPEST FLIGHTS AND SEND WSP ---------------------------------- #

# check if token is active before requesting
flight_search.refresh_token_if_needed()
    
# request the cheapest flight from each city in the sheety
for city in sheety_data['prices']:
    time.sleep(2)
    flights = flight_search.search_flights(DEPARTURE_IATA_CODE,
                                           city['iataCode'],
                                           tomorrow.strftime('%Y-%m-%d'),
                                           six_month_from_today.strftime('%Y-%m-%d'))
    cheapest_flight = find_cheapest_flight(flights)
    # if cheapest flight is found send it as a wsp message
    if cheapest_flight.price != "N/A" and cheapest_flight.price < city["lowestPrice"]:
        print(f"Lower price flight found to {city['city']}!")
        notification_manager.send_whatsapp(user_whatsapp_list,
            message_body=f"Low price alert! Only {cheapest_flight.price}USD to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport} - {city['city']}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )

