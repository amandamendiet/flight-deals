class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        """
        Initialize a new flight data instance with specific travel details.

        Parameters:
            price: The total cost of the flight.
            origin_airport: The IATA code for the departing airport.
            destination_airport: The IATA code for the airport of destination.
            out_date: The departure date for the flight.
            return_date: The return date for the flight.
            stops: The number of stops before reaching the destination.
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data):
    """
    Parses the flight data taken from the Amadeus API to find the cheapest flight option among from multiple entries.
    :param data:
        data (dict): The JSON data containing the flight details returned by the API.
    :return:
        FlightData: An instance of the FlightData class representing the cheapest flight found,
        or a FlightData instance where all fields are 'NA' if no valid flight data is available.

    First, this function checks if the data received has valid flight details, if no found data is found,
    it returns the FlightData object with all fields as N/A entries.

    If the entries are valid flight details, it initializes the first_flight and all the flight details as
    the first entry found in the JSON returned from the API.

    Then it iterates through the rest of the flight entries and compares their price to the first flight price.
    If it founds a cheaper price in the other entries then it updates all the variables for the flight details with
    the cheaper flight found.

    Finally, it returns the cheapest flight found as a FlightData object with all the flight details.
    """

    # Handle empty data if no flight or Amadeus rate limit exceeded
    print("Finding cheapest flight")
    if data is None or not data['data']:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    # Data from the first flight in the json
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    print(f"Lowest price: {lowest_price}")
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    # A flight with 2 segments will have 1 stop
    nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1
    destination = first_flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    # Initialize FlightData with the first flight for comparison
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)

    # Iterate each flight entry and compare its price with the first flight price
    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        # if a cheaper price is found, update the current flight details with the cheaper flight details found.
        if price < lowest_price:
            lowest_price = price
            print(f"lowest_price is now = {lowest_price}USD")
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            nr_stops = len(flight["itineraries"][0]["segments"]) - 1
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)

    print(f"Lowest price to {destination} is {lowest_price}USD")

    return cheapest_flight
