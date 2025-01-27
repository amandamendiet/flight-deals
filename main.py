#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager

# create objects
flight_search = FlightSearch()
sheety_data_manager = DataManager()

# get data from the spreadsheet
sheety_data_manager.get_sheet_data()
sheety_data = sheety_data_manager.sheety_data

# for each city in the spreadsheet GET iata code and UPDATE it in the spreadsheet
for city_info in sheety_data['prices']:
    city_info['iataCode'] = flight_search.search_cities_iata_code(city_info['city'])
    sheety_data_manager.update_city_iata_code(city_info['id'], city_info['iataCode'])


