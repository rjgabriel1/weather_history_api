from flask import Flask
from flask import render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/v1/<station>/<date>")
def get_weather(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature= df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    temp = 12
    return {"date": date,
            "station_id": station,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True,port=3000)
