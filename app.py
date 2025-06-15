from flask import Flask, render_template, request
from geopy.distance import geodesic

app = Flask(__name__)

destination = (31.25654, 32.28411)

def calculate_shipping_cost(service_type, weight, distance_km):
    base_price = {"standard": 30, "express": 50}
    km_price = {"standard": 3, "express": 5}
    return base_price[service_type] + km_price[service_type] * distance_km + 0.5 * float(weight)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        service = request.form["service"]
        weight = request.form["weight"]
        lat = float(request.form["lat"])
        lon = float(request.form["lon"])
        user_location = (lat, lon)

        distance = geodesic(user_location, destination).km
        cost = calculate_shipping_cost(service, weight, distance)
        time_days = round(distance / (60 if service == "express" else 30), 1)

        return render_template("result.html", cost=round(cost, 2), time_days=time_days)

    return render_template("index.html")

if __name__ == "__main__":
    import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
