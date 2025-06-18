from flask import Flask, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

# Данни за колите и техните ревюта
cars = [
    {
        "name": "Toyota Corolla",
        "reviews": ["Евтина и икономична", "Идеална за семейство", "Много надеждна кола"]
    },
    {
        "name": "BMW M3",
        "reviews": ["Изключително бърза и спортна", "Скъпа, но мощна", "Превъзходно управление"]
    },
    {
        "name": "Volkswagen Passat",
        "reviews": ["Удобна за дълги пътувания", "Много място вътре", "Не е много спортна"]
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    keyword = ""

    if request.method == "POST":
        keyword = request.form["keyword"].lower()
        best_car = None
        best_score = float('-inf')

        for car in cars:
            matched_reviews = []
            total_score = 0

            for review in car["reviews"]:
                if keyword in review.lower():
                    matched_reviews.append(review)
                    sentiment = analyzer.polarity_scores(review)["compound"]
                    total_score += sentiment

            if matched_reviews and total_score > best_score:
                best_score = total_score
                best_car = {
                    "name": car["name"],
                    "matched_reviews": matched_reviews
                }

        result = best_car

    return render_template("index.html", result=result, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)
