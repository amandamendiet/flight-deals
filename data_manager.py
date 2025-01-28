import os
from dotenv import load_dotenv
import requests

# load env variable from env file
load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.SHEETY_PRICES_ENDPOINT = os.environ.get("SHEETY_PRICES_ENDPOINT")
        self.SHEETY_USERS_ENDPOINT = os.environ.get("SHEETY_USERS_ENDPOINT")
        self.SHEETY_USERNAME = os.environ.get("SHEETY_USERNAME")
        self.SHEETY_PASSWORD = os.environ.get("SHEETY_PASSWORD")
        self.SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
        self.SHEETY_HEADERS = {
            'Authorization':self.SHEETY_TOKEN
        }
        self.sheety_destination_data = {}
        self.sheety_user_data = {}

    def get_sheet_data(self):
        print("Getting sheet data")
        response = requests.get(url=self.SHEETY_PRICES_ENDPOINT, headers=self.SHEETY_HEADERS)
        self.sheety_destination_data = response.json()


    def update_city_iata_code(self, id, iata_code):
        print(f"Updating iata code: {iata_code}")
        return requests.put(url=f"{self.SHEETY_PRICES_ENDPOINT}/{id}",
                            headers=self.SHEETY_HEADERS,
                            json={'price':{'iataCode':iata_code}})


    def get_user_whatsapp_number(self):
        print("Getting users Whatsapp number")
        response = requests.get(url=self.SHEETY_USERS_ENDPOINT)
        data = response.json()
        self.sheety_user_data = data["users"]
        return self.sheety_user_data