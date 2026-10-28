from flask import Flask, render_template, request
from recommender import recommend_recipes

app = Flask(__name__)

@app.route("/", methods =["GET", "POST"])
def index():
    recipes = []
    ingredients_input = ""

    if request.method == "POST":
        ingredients_input = request.form.get("ingredients", "")
        ingredients = ingredients_input.split(",")

        recipes = recommend_recipes(ingredients)

    return render_template(
        "index.html",
        recipes = recipes,
        ingredients_input = ingredients_input
    )

if __name__ == "__main__":
    app.run(debug = True)
