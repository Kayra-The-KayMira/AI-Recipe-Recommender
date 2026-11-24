
from sentence_transformers import SentenceTransformer, util

# Store previously calculated embeddings
EMBEDDING_CACHE = {}

RECIPE_EMBEDDING_CACHE = {}

# Load the embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# Known ingredient synonyms
INGREDIENT_ALIASES = {
    "aubergine": "eggplant",
    "courgette": "zucchini",
    "coriander": "cilantro"
}


def normalize_ingredient(ingredient):
    ingredient = ingredient.strip().lower()

    return INGREDIENT_ALIASES.get(
        ingredient,
        ingredient
    )

def get_embedding(ingredient):

    ingredient = normalize_ingredient(ingredient)

    if ingredient not in EMBEDDING_CACHE:
        EMBEDDING_CACHE[ingredient] = model.encode(
            ingredient,
            convert_to_tensor=True
        )

    return EMBEDDING_CACHE[ingredient]


def get_recipe_embedding(recipe):

    ingredients = recipe.get("ingredients", [])

    if not isinstance(ingredients, (list, tuple, set)):
        return None

    normalized_ingredients = tuple(sorted({
        normalize_ingredient(ingredient)
        for ingredient in ingredients
        if isinstance(ingredient, str) and ingredient.strip()
    }))

    if not normalized_ingredients:
        return None

    if normalized_ingredients not in RECIPE_EMBEDDING_CACHE:

        recipe_text = "Ingredients: " + ", ".join(
            normalized_ingredients
        )

        RECIPE_EMBEDDING_CACHE[normalized_ingredients] = model.encode(
            recipe_text,
            convert_to_tensor=True
        )

    return RECIPE_EMBEDDING_CACHE[normalized_ingredients]


def calculate_recipe_similarity(user_ingredients, recipe):

    if not isinstance(user_ingredients, (list, tuple, set)):
        return 0.0

    normalized_user_ingredients = sorted({
        normalize_ingredient(ingredient)
        for ingredient in user_ingredients
        if isinstance(ingredient, str) and ingredient.strip()
    })

    if not normalized_user_ingredients:
        return 0.0

    recipe_embedding = get_recipe_embedding(recipe)

    if recipe_embedding is None:
        return 0.0

    user_text = "Ingredients: " + ", ".join(
        normalized_user_ingredients
    )

    user_embedding = model.encode(
        user_text,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        user_embedding,
        recipe_embedding
    )

    return float(similarity.item())


def calculate_similarity(ingredient1, ingredient2):

    ingredient1 = normalize_ingredient(ingredient1)
    ingredient2 = normalize_ingredient(ingredient2)

    if ingredient1 == ingredient2:
        return 1.0

    embedding1 = get_embedding(ingredient1)
    embedding2 = get_embedding(ingredient2)

    similarity = util.cos_sim(
        embedding1,
        embedding2
    )

    return float(similarity.item())


if __name__ == "__main__":

    test_recipes = [
        {
            "name": "Cheese Omelette",
            "ingredients": ["egg", "cheese"]
        },
        {
            "name": "Tomato Pasta",
            "ingredients": ["tomato", "pasta"]
        },
        {
            "name": "Chocolate Cake",
            "ingredients": ["chocolate", "flour", "sugar"]
        }
    ]

    test_scenarios = [
        ["egg", "cheese"],
        ["tomato", "pasta"]
    ]

    for user_ingredients in test_scenarios:

        print("\nUser Ingredients:", user_ingredients)
        print("-" * 40)

        results = []

        for recipe in test_recipes:

            score = calculate_recipe_similarity(
                user_ingredients,
                recipe
            )

            results.append({
                "name": recipe["name"],
                "ai_similarity": score
            })

        results.sort(
            key=lambda item: item["ai_similarity"],
            reverse=True
        )

        for result in results:
            print(
                f"{result['name']}: "
                f"{result['ai_similarity']:.4f}"
            )

    print("\nCached Recipes:", len(RECIPE_EMBEDDING_CACHE))


