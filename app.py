# Import necessary modules from Flask
from flask import Flask, render_template, request, jsonify
# Import sentiment analyzer from VADER
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from flask import send_from_directory
# Create an instance of the sentiment analyzer
app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

# Sample car data with names, images, links, and user reviews
cars = [
    {
        "name": "Toyota Corolla",
        "image": "toyota corolla.jfif",
        "link": "https://www.mobile.bg/obiava-11748529363630123-toyota-corolla-1-4d",
        "reviews": [
            "Affordable and fuel-efficient",
            "Perfect for families",
            "Very reliable car",
            "Easy to maintain",
            "Smooth and quiet ride"
        ]
    },
    {
        "name": "BMW M3",
        "image": "bmw m3.jfif",
        "link": "https://www.mobile.bg/obiava-11750609537423765-bmw-m3-competition",
        "reviews": [
            "Extremely fast and sporty",
            "Expensive but powerful",
            "Handles like a dream",
            "Luxurious interior",
            "A thrill to drive"
        ]
    },
    {
        "name": "Volkswagen Passat",
        "image": "vw passat.jfif",
        "link": "https://www.mobile.bg/obiava-11740497149174873-vw-passat-lizing-1-6tdi-105ks-6-skorosti-evro-5",
        "reviews": [
            "Comfortable for long trips",
            "Lots of interior space",
            "Not very sporty",
            "Solid build quality",
            "Efficient and quiet engine"
        ]
    },
    {
        "name": "Mercedes-Benz C-Class",
        "image": "mercedes benz.jfif",
        "link": "https://www.mobile.bg/obiava-11734076006609311-mercedes-benz-c-200-amg-digital-face-de-distr-pano-camera-car-play-liz",
        "reviews": [
            "Luxury in every detail",
            "Great for business trips",
            "Quiet and smooth ride",
            "High-end technology inside",
            "A bit pricey, but worth it"
        ]
    },
    {
        "name": "Ford Mustang",
        "image": "ford mustang.jfif",
        "link": "https://www.mobile.bg/obiava-11742329052796393-ford-mustang-10-2024god",
        "reviews": [
            "Classic American muscle",
            "Powerful engine sound",
            "Great acceleration",
            "Turns heads everywhere",
            "Rear seats are a bit tight"
        ]
    },
    {
        "name": "Honda Civic",
        "image": "honda civic.jfif",
        "link": "https://www.mobile.bg/obiava-11747216958559402-honda-civic-1-0-vtec-turbo-elegance-mt",
        "reviews": [
            "Very reliable and efficient",
            "Easy to drive and park",
            "Great resale value",
            "Perfect for daily commuting",
            "Modern design and features"
        ]
    },
    {
        "name": "Tesla Model 3",
        "image": "tesla model 3.jfif",
        "link": "https://www.mobile.bg/obiava-11742388625862648-tesla-model-3-long-range-awd",
        "reviews": [
            "Instant torque and smooth ride",
            "Autopilot is a game-changer",
            "Minimalist interior design",
            "Great electric range",
            "Expensive but futuristic"
        ]
    },
    {
        "name": "Skoda Octavia",
        "image": "skoda octavia.jfif",
        "link": "https://www.mobile.bg/obiava-11751228679315393-skoda-octavia-1-6tdi-105hp-6sk-4h4",
        "reviews": [
            "Practical and spacious",
            "Great fuel economy",
            "Affordable service costs",
            "Ideal for families",
            "Well-built interior"
        ]
    },
    {
        "name": "Peugeot 3008",
        "image": "peugeot 3008.jfif",
        "link": "https://www.mobile.bg/obiava-11740994314187557-peugeot-3008-1-2i-nov-vnos",
        "reviews": [
            "Stylish SUV design",
            "Good fuel efficiency",
            "Comfortable seating",
            "Advanced infotainment system",
            "Smooth suspension"
        ]
    },
    {
        "name": "Hyundai Tucson",
        "image": "hyundai tucson.jfif",
        "link": "https://www.mobile.bg/obiava-21751107546399169-hyundai-tucson-1-6d",
        "reviews": [
            "Reliable and efficient",
            "Spacious and comfortable",
            "Great warranty coverage",
            "Good for city and off-road",
            "Modern looks"
        ]
    },
    {
        "name": "Renault Clio",
        "image": "renault clio.jfif",
        "link": "https://www.mobile.bg/obiava-11715967416167993-renault-clio-1-0",
        "reviews": [
            "Compact and agile",
            "Perfect for city driving",
            "Low fuel consumption",
            "Easy to park",
            "Good value for money"
        ]
    },
    {
        "name": "Mazda CX-5",
        "image": "mazda cx5.jfif",
        "link": "https://www.mobile.bg/obiava-21732117592198766-mazda-cx-5-2-2d-navi-kamera-lizing",
        "reviews": [
            "Fun to drive",
            "Sporty design",
            "Comfortable ride",
            "Great handling",
            "Reliable Japanese quality"
        ]
    },
    {
        "name": "Kia Sportage",
        "image": "kia sportage.jfif",
        "link": "https://www.mobile.bg/obiava-21742321161606537-kia-sportage-4x4",
        "reviews": [
            "Solid SUV for the price",
            "Plenty of space inside",
            "Good fuel efficiency",
            "Nice tech features",
            "Sleek and modern look"
        ]
    }
]

# Route to serve static HTML pages from the 'pages' directory
@app.route('/pages/<path:filename>')
def serve_page(filename):
    return send_from_directory('pages', filename)

# Route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# API route that processes user input and returns matching cars
@app.route('/GetCar', methods=["GET", "POST"])
def GetCar():
    # Get the keyword entered by the user
    keyword = request.form.get("keyword", "").lower()
    filtered_cars = []

 # Check each car's reviews for a match with the keyword
    for car in cars:
        matched_reviews = [review for review in car["reviews"] if keyword in review.lower()]
        if matched_reviews:
            filtered_cars.append({
                "name": car["name"],
                "image": car.get("image", ""),
                "link": car.get("link", ""),
                "matched_reviews": matched_reviews # Include only matching reviews
            })

# Limit the result to the first 3 matching cars
    result = filtered_cars[:3] if filtered_cars else []
# Return the result as JSON
    return jsonify({"result": result, "keyword": keyword})


# Run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)