#!/usr/bin/env python3

import googlemaps
from pathlib import Path
import os

THIS_DIR = Path(os.path.realpath(__file__)).parent

# read in destinations, ignoring comments and blank lines
with (THIS_DIR / "desinations.txt").open('r') as f:
    uncommented = [ line.split('#')[0].strip() for line in f.readlines() ]
destinations = filter(None, uncommented)

# activate the google maps api
with (THIS_DIR / "apikey.txt").open('r') as f:
    gmaps = googlemaps.Client(key=f.read().strip())


