import lastcall
from urllib.parse import unquote

from flask import Flask, render_template, g
from flask.ext.moment import Moment
app = Flask(__name__)
moment = Moment(app)

@app.route("/")
def enter_station():
    return render_template("enter_station.html", destinations=lastcall.read_destinations())

@app.route("/custom/<station>")
def show_station(station):
    station = unquote(station)
    return render_template("show_station.html", station=station, routes=lastcall.get_route_options(g, station))

if __name__ == "__main__":
    g = lastcall.setup_maps()
    app.run(debug=True, host="0.0.0.0", port=80)
