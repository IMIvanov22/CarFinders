from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import send_from_directory
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

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
        "reviews": [
            "Comfortable for long trips",
            "Lots of interior space",
            "Not very sporty",
            "Solid build quality",
            "Efficient and quiet engine"
        ]
    },
    {
        "name": "Audi A4",
        "reviews": [
            "Very smooth driving experience",
            "High-quality interior",
            "Excellent fuel economy",
            "Packed with features",
            "Feels premium inside and out"
        ]
    },
    {
        "name": "Mercedes-Benz C-Class",
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
        "reviews": [
            "Instant torque and smooth ride",
            "Autopilot is a game-changer",
            "Minimalist interior design",
            "Great electric range",
            "Expensive but futuristic"
        ]
    }
]

@app.route('/pages/<path:filename>')
def serve_page(filename):
    return send_from_directory('pages', filename)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/GetCar', methods=["GET", "POST"])
def GetCar():
    keyword = request.form.get("keyword", "").lower()
    filtered_cars = []

    for car in cars:
        matched_reviews = [review for review in car["reviews"] if keyword in review.lower()]
        if matched_reviews:
            filtered_cars.append({
                "name": car["name"],
                "image": car.get("image", ""),
                "link": car.get("link", ""),
                "matched_reviews": matched_reviews
            })

    result = filtered_cars[:3] if filtered_cars else []
    return jsonify({"result": result, "keyword": keyword})

if __name__ == "__main__":
    app.run(debug=True)