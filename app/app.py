import os
import glob
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

import numpy as np
import pandas as pd
import gmplot
from colour import Color
from process_file import process_data
import geocoder

UPLOAD_FOLDER = './app/tmp/'
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = glob.glob(app.config['UPLOAD_FOLDER'] + '*')
        map_filepath = "./app/templates/city_wait.html"
        files += glob.glob(map_filepath)
        for f in files:
            os.remove(f)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Data Visualization with Google Maps</title>
    <link href="./static/bootstrap.min.css" rel="stylesheet" media="screen">
    <h1><center>Data Visualization with Google Maps</h1>
    <h4><center>Upload new file</h4>
    <form action="" method=post enctype=multipart/form-data><center>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p><center>%s</p>
    <form action="/render_map" method=post>
         <input type=submit value="Render map">
    </form>
    """ % "<br>".join(
        [os.path.basename(f) for f in
        glob.glob(app.config['UPLOAD_FOLDER'] + '*.csv') +
        glob.glob(app.config['UPLOAD_FOLDER'] + '*.xls') +
        glob.glob(app.config['UPLOAD_FOLDER'] + '*.xlsx')])

@app.route('/render_map', methods=['GET', 'POST'])
def render_map():
    if request.method == 'POST':
        file = glob.glob(app.config['UPLOAD_FOLDER'] + '*')[0]
        map_filepath = "./app/templates/city_wait.html"

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

            green = Color("white")
            colors = list(green.range_to(Color("black"), len(wait_avg)))
            colors = [c.hex for c in colors]

            sizes = [SIZE_CONSTANT * w[1][1] for w in wait_avg] # based on
                    # number of mentees

            for i in xrange(len(lats)):
                gmap.scatter(
                        [lats[i]], [lngs[i]], colors[i], size=sizes[i],
                        marker=False)

            gmap.draw(map_filepath)

        if not os.path.exists(map_filepath):
            wait_avg = process_data(file)
            map_data(wait_avg)

        return render_template('city_wait.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
