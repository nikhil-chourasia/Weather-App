from flask import *
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

def conversion(f):
    return f"{round((f-32)*5/9, 1)}°C"

@app.route("/", methods=["GET", "POST"])


def index():

    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            load_dotenv()

            YOUR_API_KEY = os.getenv('YOUR_API_KEY')

            url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=us&key={YOUR_API_KEY}&contentType=json'

            responses = requests.get(url=url)
            data = responses.json()
            weather_data = {
                "city": city,
                "description": data["days"][0]["description"],
                "temp": conversion(data["days"][0]["temp"]),
                "feel": conversion(data["days"][0]["feelslike"]),
                "rain": f"{data["days"][0]["precip"]}%",
                "uv": data["days"][0]["uvindex"],
                "conditions": data["days"][0]["conditions"],
                "wind": data["days"][0]["windspeed"],
                "humidity": data["days"][0]["humidity"]
            }

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)