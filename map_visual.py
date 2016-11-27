import numpy as np
import pandas as pd
import gmplot
from colour import Color
from visual import process_data
import geocoder

ZOOM_SIZE = 11
SIZE_CONSTANT = 20
ADDRESS_AFFIX = ", MA"

def location(city):
    google = geocoder.google(city).latlng
    if len(google) > 0:
        return google
    else:
        o = geocoder.osm(city)
        return [o.osm["y"], o.osm["x"]]

def map_data(wait_avg):
    # convert dict to list of tuples sorted on avg wait time
    wait_avg = sorted(wait_avg.items(), key=lambda x: x[1][0])
    cities = [w[0] + ADDRESS_AFFIX for w in wait_avg]
    locs = [location(x) for x in cities]

    lats = [loc[0] for loc in locs]
    lngs = [loc[1] for loc in locs]

    lat_center = sum(lats) / len(lats)
    lng_center = sum(lngs) / len(lngs)

    zoom_size = ZOOM_SIZE

    gmap = gmplot.GoogleMapPlotter(lat_center, lng_center, zoom_size)

    green = Color("green")
    colors = list(green.range_to(Color("red"), len(wait_avg)))
    colors = [c.hex for c in colors]

    sizes = [SIZE_CONSTANT * w[1][1] for w in wait_avg] # based on number of mentees

    for i in xrange(len(lats)):
        gmap.scatter([lats[i]], [lngs[i]], colors[i], size=sizes[i], marker=False)

    gmap.draw("city_wait.html")

wait_avg = process_data('waitlist.csv')
map_data(wait_avg)
