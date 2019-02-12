from pprint import pformat
import os

import requests
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"



GOOGLE_KEY = os.environ.get('GOOGLE_KEY')

# GOOGLE_URL_1 = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_KEY+"&callback=initMap"
# GOOGLE_URL_2 = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_KEY+"&libraries=places&callback=initMap" 
# GOOGLE_URL_3 = "https://maps.googleapis.com/maps/api/place/findplacefromtext/output?key="+GOOGLE_KEY+"&input=coit tower&inputtype=textquery"
# GOOGLE_URL_4 = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key="+GOOGLE_KEY
# GOOGLE_URL_5 = <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key="+GOOGLE_KEY+"&libraries=places"></script>
# #<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"></script>

@app.route("/")
def homepage():
    """Show homepage."""
    #EF: include log in screen!

    return render_template("homepage.html")

@app.route("/new-submission")
def new_submission():
    """Show form submission page."""
    
    return render_template("new_submission.html")

@app.route("/my-map", methods=["POST"])
def my_map():
    """Show homepage."""
    pass
    return render_template("my_map.html")


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    os.system("source secrets.sh") #applies API key to environ at run time
    app.run(host="0.0.0.0")