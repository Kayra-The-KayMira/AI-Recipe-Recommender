RECIPES = [
    {
        "name": "Cheese Omlette",
        "ingredients": ["egg", "cheese"],
        "instruction": "Beat the eggs, add cheese, and cook in a pan.",
        "cooking_time": 10
    },
    {
        "name": "Tomato Pasta",
        "ingredients": ["tomato", "pasta"],
        "instruction": "Cook the pasta. Prepare a tomato sauce and mix them.",
        "cooking_time": 20
    },
    {
        "name": "Vegetable Omelette",
        "ingredients": ["egg", "tomato", "pepper"],
        "instruction": "Chop the vegetables, beat the eggs, and cook everything in a pan",
        "cooking_time": 10
    },
    {
        "name": "Cheese Sandwich",
        "ingredients": ["bread", "cheese", "tomato"],
        "instructions": "Place cheese and sliced tomato between bread slices",
        "cooking_time": 5
    }
]
def recommend_recipes(user_ingredients):
    user_ingredients = {
        ingredient.strip().lower()
        for ingredient in user_ingredients
        if ingredient.strip()
    }

    recommendations = []

    for recipe in RECIPES:
        recipe_ingredients = set(recipe["ingredients"])
        matching_ingredients = user_ingredients.intersection(
            recipe_ingredients
        )

        if matching_ingredients:
            recommendations.append({
                **recipe,
                "matching_ingredients": sorted(matching_ingredients),
                "missing_ingredients": sorted(recipe_ingredients - user_ingredients),
                "match_count": len(matching_ingredients)
            })

    recommendations.sort(
        key = lambda recipe: (
            -recipe["match_count"],
            len(recipe["missing_ingredients"])
        )
    )

    return recommendations