from flask import Flask
from flask import render_template
from flask import jsonify
import pandas as pd

app = Flask(__name__)



stations = pd.read_csv('./data_small/stations.txt', skiprows=17)
print(stations)


@app.route("/")
def home():
    return render_template('index.html', data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def get_weather(station, date):
    filename = "./data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # filtering file to render temperature based on given date and station id
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {"date": date,
            "station_id": station,
            "temperature": temperature}


# Get all data for station
@app.route("/api/v1/<station_id>")
def all_data(station_id):
    filename = "./data_small/TG_STAID" + str(station_id).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient='records')
    return jsonify(result)


@app.route("/api/v1/annual/<station>/<year>")
def yearly(station, year):
    filename = "./data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, )
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))]
    result = result.to_dict(orient='records')
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=7000)
