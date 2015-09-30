#!/usr/bin/env python3

import googlemaps
import os
from collections import namedtuple
from datetime import datetime, timedelta
from pathlib import Path

Route = namedtuple("Route", ["depart", "arrive"])

def source_file(filename):
    '''Identify a file distributed with the project's source.'''
    return Path(os.path.realpath(__file__)).parent / filename

def read_source():
    '''Read in the physical location of the display system.'''

    # use the source location distributed with the project's source
    with source_file("source.txt").open('r') as f:
        return f.read().strip()

def read_destinations():
    '''Read in destinations from file, ignoring comments and blank lines.'''

    # use the destination addresses distributed with the project's source
    with source_file("destinations.txt").open('r') as f:

        # strip anything after a hash in each line
        uncommented = [ line.split('#')[0].strip() for line in f.readlines() ]

    # remove blank lines
    return list(filter(bool, uncommented))

def setup_maps() -> googlemaps.Client:
    '''Activate the Google Maps API.'''

    # use the API key distributed with the project's source
    with source_file("apikey.txt").open('r') as f:

        # sanitize and activate the key
        return googlemaps.Client(key=f.read().strip())

def find_route_times(api_client, req_departure: datetime, destination, source=read_source()) -> Route:
    '''Gets arrival and departure times after a given time for a destination,
    if leaving from the space. Pads departure by ten minutes, so "leaving now"
    assumes it'll be ten minutes until you walk out the front door.'''

    # We need to query for a departure time ten minutes after the time actually
    # requested. It takes at least this long to get out of the space.
    req_departure += timedelta(minutes=10)

    # query Google Maps for a route
    routes = api_client.directions(source, destination, mode="transit",
            language="nl", units="metric", region="nl",
            departure_time=req_departure)

    # parse the Maps response
    route_raw = routes[0]["legs"][-1]
    try:
        departure = datetime.fromtimestamp(route_raw["departure_time"]["value"])
        arrival = datetime.fromtimestamp(route_raw["arrival_time"]["value"])
    except KeyError: # no route found
        return

    # Tell the user to leave ten minutes before Google's time of departure.
    # This complements the ten minutes we added above.
    departure -= timedelta(minutes=10)

    return Route(departure, arrival)

def largest_key_each_value(pairs: [("key", "value")]) -> [("key", "value")]:
    '''Given a list of key-value pairs, sort it so that the largest keys for
    each given value are retained, dropping all other keys for that value.'''

    # preserve the input type
    orig_type = type(pairs[0])

    # sort the key-value pairs by key, increasing
    pairs = sorted(pairs, key=lambda x: x[0])

    # put the pairs in a dictionary with the mapping inverted
    inverse_map = { v: k for k, v in pairs }

    # This inverted map does the hard work. Because we just sorted the pairs,
    # largest keys will be inserted later, and because dictionaries throw out
    # old mappings in favor of more recently inserted ones, only the largest
    # keys for each value will be retained.

    # put the pairs back in the input type and format
    return [ orig_type(k, v) for v, k in sorted(inverse_map.items(), key=lambda x: x[0]) ]

def get_options(api_client, destination, now=datetime.now()) -> [Route]:
    '''Finds arrival times if you were to pack up between ten minutes and an
    hour from now, in intervals of ten minutes. (0, 10, 20, 30, 40, 50)'''

    # create the list of times to query
    times = [ now + timedelta(minutes=td) for td in range(0, 60, 10) ]

    # check for routing at each time
    routes_raw = [ find_route_times(api_client, t, destination) for t in times ]

    # remove empty responses
    routes = list(filter(bool, routes_raw))

    # bail if nothing's availble
    if not routes: return

    # if two routes arrive at the same time, choose the one that leaves later
    return [ Route(d, a) for d, a in largest_key_each_value(routes) ]

def cli_result_display(routes: [Route]):
    '''Pretty-print results into a 13 width by 6 height faux-terminal.'''

    print(" _______________\n/               \\")
    fmt = "%H:%M"

    if routes:
        for route in routes:
            print('|', route.depart.strftime(fmt), '-', route.arrive.strftime(fmt), '|')
    else:
        print("|               |\n|  No transit!  |\n|               |")

    print("\_______________/\n")

################################################################################

DEST = "Den Haag HS, 2515 Den Haag"
gmaps = setup_maps()
print("\nDisplayed now:")
cli_result_display(get_options(gmaps, DEST))
print("\nDisplayed at ten-thirty:")
cli_result_display(get_options(gmaps, DEST, now=datetime(2015, 10, 5, hour=10, minute=30)))
print("\nDisplayed at twenty-two hundred:")
cli_result_display(get_options(gmaps, DEST, now=datetime(2015, 10, 5, hour=22)))
print("\nDisplayed at midnight:")
cli_result_display(get_options(gmaps, DEST, now=datetime(2015, 10, 5)))
