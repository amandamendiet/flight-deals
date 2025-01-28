import os
from dotenv import load_dotenv
import requests

# load env variable from env file
load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.SHEETY_ENDPOINT = "https://api.sheety.co/1bfb2d6e09148818451627bf99059c65/flightDeals/prices"
        self.SHEETY_USERNAME = os.environ.get("SHEETY_USERNAME")
        self.SHEETY_PASSWORD = os.environ.get("SHEETY_PASSWORD")
        self.SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
        self.SHEETY_HEADERS = {
            'Authorization':self.SHEETY_TOKEN
        }
        self.sheety_data = {}


    def get_sheet_data(self):
        print("getting sheet data")
        response = requests.get(url=self.SHEETY_ENDPOINT, headers=self.SHEETY_HEADERS)
        self.sheety_data = response.json()


    def update_city_iata_code(self, id, iata_code):
        print(f"updating iata code: {iata_code}")
        return requests.put(url=f"{self.SHEETY_ENDPOINT}/{id}",
                                     headers=self.SHEETY_HEADERS,
                                     json={'price':{'iataCode':iata_code}})

