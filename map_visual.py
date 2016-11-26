import numpy as np
import pandas as pd
import gmplot

def map_data(wait_avg):

    cities = wait_avg.keys()
    locs = [location(x) for x in cities]
    lats = [loc[0] for loc in locs]
    lngs = [loc[1] for loc in locs]

    lat_center = sum(lats)/len(lats)
    lng_center = sum(lngs)/len(lngs)

    # need to specify this still, check to see how it looks
    zoom_size = 16

    gmap = gmplot.GoogleMapPlotter(lat_center, lng_center, zoom_size)
    # need to specify this still, use external package
    colors = []
    sizes = [10*wait_avg[x][1] for x in wait_avg]
    for i in range(len(lats)):
	gmap.scatter([lats[i]], [lngs[i]], colors[i], size=sizes, marker=False)

    gmap.draw("city_wait.html")


def location(city):
    params = {
            'address' : city,
            'sensor' : 'false',
    }
    url = 'http://maps.google.com/maps/api/geocode/json?%s' %(
        urllib.urlencode(params),)
    response = urllib2.urlopen(url)
    result = json.load(response)
    try:
            lat_lng_dict = result['results'][0]['geometry']['location']
            return (lat_lng_dict['lat'], lat_lng_dict['lng'])
    except:
            return ()
