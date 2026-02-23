from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)
model = None  # will load on first request

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    global model
    if model is None:
        try:
            model = joblib.load("wine_model.pkl")
        except Exception as e:
            return f"Error loading model: {e}"

    try:
        features = [
            float(request.form["fixed_acidity"]),
            float(request.form["volatile_acidity"]),
            float(request.form["citric_acid"]),
            float(request.form["residual_sugar"]),
            float(request.form["chlorides"]),
            float(request.form["free_sulfur_dioxide"]),
            float(request.form["total_sulfur_dioxide"]),
            float(request.form["density"]),
            float(request.form["pH"]),
            float(request.form["sulfates"]),
            float(request.form["alcohol"])
        ]

        prediction = model.predict([features])
        result = round(prediction[0], 2)
        return render_template("index.html", prediction_text=f"Predicted Wine Quality: {result}")
    except Exception as e:
        return f"Error occurred during prediction: {e}"

# Health check route for Heroku
@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    # Use dynamic port for Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)