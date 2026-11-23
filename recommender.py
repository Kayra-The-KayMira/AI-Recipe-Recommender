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
def recommend_recipes(user_ingredients, max_cooking_time = None):
    user_ingredients = {
        ingredient.strip().lower()
        for ingredient in user_ingredients
        if ingredient.strip()
    }

    recommendations = []

    for recipe in RECIPES:

        if max_cooking_time is not None:
            if recipe["cooking_time"] > max_cooking_time:
                continue

        recipe_ingredients = {
            ingredient.strip().lower()
            for ingredient in recipe['ingredients']
        }

        matching_ingredients = user_ingredients.intersection(
            recipe_ingredients
        )

        missing_ingredients = recipe_ingredients - user_ingredients

        if matching_ingredients:

            match_percentage = (len(matching_ingredients) / len(recipe_ingredients)) * 100

            recommendations.append({
                **recipe,
                "matching_ingredients": sorted(matching_ingredients),
                "missing_ingredients": sorted(missing_ingredients),
                "match_count": len(matching_ingredients),
                "match_percentage": round(match_percentage, 2),
                "is_complete": len(missing_ingredients) == 0
            })

    recommendations.sort(
        key = lambda recipe: (
            -recipe["match_count"],
            -recipe["match_percentage"],
            len(recipe["missing_ingredients"]),
            recipe["cooking_time"]
        )
    )

    return recommendations

if __name__ == "__main__":
    test_ingredients = ["egg", "tomato"]

    result = recommend_recipes(test_ingredients, max_cooking_time = 10)

    for recipe in result:
        print(f"Recipe: {recipe['name']}")
        print(f"Match: {recipe['match_percentage']}%")
        print(f"Matching ingredients: {recipe['matching_ingredients']}")
        print(f"Missing ingredients: {recipe['missing_ingredients']}")
        print(f"Can cook now: {recipe['is_complete']}")
        print("-" * 30)
