import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.AMADEUS_API_KEY = os.environ.get("AMADEUS_API_KEY")
        self.AMADEUS_API_SECRET = os.environ.get("AMADEUS_API_SECRET")
        self.AMADEUS_TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.AMADEUS_TOKEN_PARAMS = {
            'grant_type': 'client_credentials',
            'client_id': self.AMADEUS_API_KEY,
            'client_secret': self.AMADEUS_API_SECRET,
        }
        self.AMADEUS_TOKEN_HEADERS = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        self.amadeus_token = os.environ.get("AMADEUS_API_TOKEN")
        self.amadeus_token_expiration = os.environ.get("AMADEUS_TOKEN_EXPIRATION")
        self.last_token_time = os.environ.get("LAST_TOKEN_TIME")
        self.AMADEUS_CITIES_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        self.AMADEUS_CITIES_HEADERS = {
            'accept':'application/vnd.amadeus+json',
            'Authorization':f"Bearer {self.amadeus_token}",
        }


    def refresh_token_if_needed(self):
        current_time = time.time()
        if current_time - int(float(self.last_token_time)) >= int(self.amadeus_token_expiration):
            self.get_new_amadeus_token()
            self.last_token_time = current_time
            self.update_env_file("LAST_TOKEN_TIME", current_time)


    def get_new_amadeus_token(self):
        response = requests.post(url=self.AMADEUS_TOKEN_ENDPOINT, headers=self.AMADEUS_TOKEN_HEADERS, data=self.AMADEUS_TOKEN_PARAMS)
        print(response.json())
        token = response.json()['access_token']
        self.amadeus_token_expiration = int(response.json()['expires_in'])
        self.update_env_file("AMADEUS_API_TOKEN", token)
        self.update_env_file("AMADEUS_TOKEN_EXPIRATION", self.amadeus_token_expiration)


    @staticmethod
    def update_env_file(token_item, new_token_info):
        with open(".env", "r") as env:
            lines = env.readlines()
        with open(".env", "w") as env:
            for line in lines:
                if line.startswith(token_item):
                    env.write(f"{token_item}={new_token_info}\n")
                else:
                    env.write(line)

    def search_cities_iata_code(self, city):
        self.refresh_token_if_needed()
        response = requests.get(url=self.AMADEUS_CITIES_ENDPOINT,
                                headers=self.AMADEUS_CITIES_HEADERS,
                                params={
                                    'keyword': city,
                                    'max':1,
                                })
        try:
            code = response.json()['data'][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city}")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}")
            return "Not Found"

        return code


    def search_flights(self):
        self.refresh_token_if_needed()


