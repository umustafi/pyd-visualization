import os
import glob
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = './tmp/'
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
        for f in files:
            os.remove(f)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title><center>Data Visualization with Google Maps</title>
    <link href="./static/bootstrap.min.css" rel="stylesheet" media="screen">
    <h1><center>Data Visualization with Google Maps</h1>
    <h4><center>Upload new file</h4>
    <form action="" method=post enctype=multipart/form-data><center>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p><center>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
