#!/usr/bin/env python3

import lastcall
from datetime import datetime

DEST = "Den Haag HS, 2515 Den Haag"
gmaps = lastcall.setup_maps()
show = lastcall.cli_result_display

print("\nDisplayed now:")
show(lastcall.get_route_options(gmaps, DEST))

print("\nDisplayed at ten-thirty:")
show(lastcall.get_route_options(gmaps, DEST, now=datetime(2015, 10, 5, hour=10, minute=30)))

print("\nDisplayed at twenty-two hundred:")
show(lastcall.get_route_options(gmaps, DEST, now=datetime(2015, 10, 5, hour=22)))

print("\nDisplayed at midnight:")
show(lastcall.get_route_options(gmaps, DEST, now=datetime(2015, 10, 5)))
