import os
from dotenv import load_dotenv
import requests
import time

# load env variable from env file
load_dotenv()
# create a time buffer for the expiration of the token
TOKEN_BUFFER = 10

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.AMADEUS_API_KEY = os.environ.get("AMADEUS_API_KEY")
        self.AMADEUS_API_SECRET = os.environ.get("AMADEUS_API_SECRET")
        self.AMADEUS_TOKEN_ENDPOINT = os.environ.get("AMADEUS_TOKEN_ENDPOINT")
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
        self.AMADEUS_CITIES_ENDPOINT = os.environ.get("AMADEUS_CITIES_ENDPOINT")
        self.AMADEUS_CITIES_HEADERS = {
            'accept':'application/vnd.amadeus+json',
            'Authorization':f"Bearer {self.amadeus_token}",
        }
        self.AMADEUS_SEARCH_ENDPOINT = os.environ.get("AMADEUS_SEARCH_ENDPOINT")
        self.AMADEUS_SEARCH_HEADERS = {
            'accept':'application/vnd.amadeus+json',
            'Authorization': f"Bearer {self.amadeus_token}",
        }


    def refresh_token_if_needed(self):
        print("Refresing token if needed")
        current_time = time.time()
        if current_time - int(float(self.last_token_time)) >= int(self.amadeus_token_expiration) - TOKEN_BUFFER:
            self.get_new_amadeus_token()
            self.last_token_time = current_time
            self.update_env_file("LAST_TOKEN_TIME", current_time)
            return True


    def get_new_amadeus_token(self):
        print("Getting new token")
        response = requests.post(url=self.AMADEUS_TOKEN_ENDPOINT, headers=self.AMADEUS_TOKEN_HEADERS, data=self.AMADEUS_TOKEN_PARAMS)
        print(response.json())
        token = response.json()['access_token']
        self.amadeus_token_expiration = int(response.json()['expires_in'])
        self.update_env_file("AMADEUS_API_TOKEN", token)
        self.update_env_file("AMADEUS_TOKEN_EXPIRATION", self.amadeus_token_expiration)
        time.sleep(2)


    @staticmethod
    def update_env_file(token_item, new_token_info):
        print("updating env file")
        with open(".env", "r") as env:
            lines = env.readlines()
        with open(".env", "w") as env:
            for line in lines:
                if line.startswith(token_item):
                    print(f"updating {token_item} in the env file")
                    env.write(f"{token_item}={new_token_info}\n")
                else:
                    env.write(line)


    def search_cities_iata_code(self, city):
        print(f"searching iata code for {city}")
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
            print(response.json())
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}")
            print(response.json())
            return "Not Found"

        return code


    def search_flights(self, origin_airport, destination_airport, out_date, return_date, is_direct=True):
        print("Searching flights")
        amadeus_search_params = {
            'originLocationCode':origin_airport,
            'destinationLocationCode':destination_airport,
            'departureDate':out_date,
            'returnDate':return_date,
            'adults':1,
            'currencyCode':'USD',
            'nonStop': "true" if is_direct else "false",
            'max':10,
        }
        response = requests.get(url=self.AMADEUS_SEARCH_ENDPOINT,headers=self.AMADEUS_SEARCH_HEADERS,params=amadeus_search_params)
        if response.status_code != 200:
            print(f"search_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference")
            print("Response body:", response.text)
            return None

        return response.json()

