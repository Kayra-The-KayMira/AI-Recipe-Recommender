
import json
from pathlib import Path


# Recipe dataset file
DATA_FILE = Path(__file__).parent / "recipes.json"


def load_recipes():
    """Load recipes from the JSON dataset."""

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            recipes = json.load(file)

        if not isinstance(recipes, list):
            raise ValueError("Recipe data must be a list.")

        return recipes

    except FileNotFoundError:
        print("Error: recipes.json file not found.")
        return []

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return []


def clean_recipes(recipes):
    """Validate and clean recipe information."""

    cleaned_recipes = []

    for recipe in recipes:

        if not isinstance(recipe, dict):
            continue

        name = recipe.get("name")
        ingredients = recipe.get("ingredients")
        instructions = recipe.get("instructions")
        cooking_time = recipe.get("cooking_time")
        category = recipe.get("category")
        servings = recipe.get("servings")

        # Check required information
        if not all([
            isinstance(name, str) and name.strip(),
            isinstance(ingredients, list) and ingredients,
            isinstance(instructions, str) and instructions.strip(),
            isinstance(category, str) and category.strip()
        ]):
            continue

        # Validate cooking time
        if (
            not isinstance(cooking_time, (int, float))
            or isinstance(cooking_time, bool)
            or cooking_time <= 0
        ):
            continue

        # Validate servings
        if (
            not isinstance(servings, int)
            or isinstance(servings, bool)
            or servings <= 0
        ):
            continue

        # Clean ingredient names
        cleaned_ingredients = []

        for ingredient in ingredients:
            if isinstance(ingredient, str) and ingredient.strip():
                cleaned_ingredient = ingredient.strip().lower()

                if cleaned_ingredient not in cleaned_ingredients:
                    cleaned_ingredients.append(cleaned_ingredient)

        if not cleaned_ingredients:
            continue

        # Create cleaned recipe
        cleaned_recipe = {
            "name": name.strip(),
            "ingredients": cleaned_ingredients,
            "instructions": instructions.strip(),
            "cooking_time": cooking_time,
            "category": category.strip(),
            "servings": servings
        }

        cleaned_recipes.append(cleaned_recipe)

    return cleaned_recipes


def process_recipes():
    """Load and clean all recipes."""

    recipes = load_recipes()
    cleaned_recipes = clean_recipes(recipes)

    print(f"Total recipes: {len(recipes)}")
    print(f"Valid recipes: {len(cleaned_recipes)}")
    print(f"Removed recipes: {len(recipes) - len(cleaned_recipes)}")

    return cleaned_recipes


if __name__ == "__main__":
    processed_recipes = process_recipes()

    print("\nCleaned Recipe Dataset:")

    for recipe in processed_recipes:
        print(f"\nRecipe: {recipe['name']}")
        print(f"Ingredients: {recipe['ingredients']}")
        print(f"Cooking time: {recipe['cooking_time']} minutes")
        print(f"Category: {recipe['category']}")
        print(f"Servings: {recipe['servings']}")
