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
def recommend_recipes(user_ingredients, max_cooking_time = None, recipes = None):

    if not isinstance(user_ingredients, (list, tuple, set)):
        return[]

    if max_cooking_time is not None:
        if isinstance(max_cooking_time, bool):
            return []
        
        if not isinstance(max_cooking_time, (int, float)):
            return[]

        if max_cooking_time < 0:
            return[]
    
    user_ingredients = {
        ingredient.strip().lower()
        for ingredient in user_ingredients
        if isinstance(ingredient, str) and ingredient.strip()
    }

    if not user_ingredients:
        return[]

    if recipes is None:
        recipes = RECIPES

    if not isinstance(recipes, (list, tuple)):
        return[]

    if not recipes:
        return[]

    recommendations = []

    for recipe in recipes:

        if max_cooking_time is not None:
            if recipe["cooking_time"] > max_cooking_time:
                continue

        recipe_ingredients = {
            ingredient.strip().lower()
            for ingredient in recipe['ingredients']
        }

        if not recipe_ingredients:
            continue

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

    cooking_time = [recipe["cooking_time"] for recipe in recipes]

    min_time = min(cooking_time)
    max_time = max(cooking_time)

    for recipe in recommendations:

        if max_time == min_time:
            time_score = 100
        else:
            time_score = ((max_time - recipe["cooking_time"]) / (max_time - min_time)) * 100

        recommendation_score = (recipe["match_percentage"] * 0.8 + time_score * 0.2)

        recipe["time_score"] = round(time_score, 2)
        recipe["recommendation_score"] = round(recommendation_score, 2)

    recommendations.sort(
        key = lambda recipe: (
            -recipe["recommendation_score"],
            -recipe["match_percentage"],
            recipe["cooking_time"]
        )
    )

    return recommendations