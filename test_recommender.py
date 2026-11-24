
import unittest

from recommender import recommend_recipes
from embedding_recommender import calculate_recipe_similarity

class TestRecommendRecipes(unittest.TestCase):

    def setUp(self):
        self.recipes = [
            {
                "name": "Test Omelette",
                "ingredients": ["egg", "cheese"],
                "cooking_time": 10
            },
            {
                "name": "Test Pasta",
                "ingredients": ["egg", "cheese", "tomato", "pasta"],
                "cooking_time": 20
            }
        ]

    def test_empty_ingredients(self):
        result = recommend_recipes([], recipes=self.recipes)
        self.assertEqual(result, [])

    def test_invalid_input(self):
        result = recommend_recipes(123, recipes=self.recipes)
        self.assertEqual(result, [])

    def test_perfect_match(self):
        result = recommend_recipes(
            ["egg", "cheese"],
            recipes=self.recipes
        )

        self.assertEqual(result[0]["match_percentage"], 100.0)
        self.assertTrue(result[0]["is_complete"])

    def test_missing_ingredients(self):
        result = recommend_recipes(
            ["egg", "cheese"],
            recipes=self.recipes
        )

        pasta = next(
            recipe for recipe in result
            if recipe["name"] == "Test Pasta"
        )

        self.assertEqual(
            pasta["missing_ingredients"],
            ["pasta", "tomato"]
        )

    def test_recommendation_score(self):
        result = recommend_recipes(
            ["egg", "cheese"],
            recipes=self.recipes
        )

        self.assertEqual(
            result[0]["recommendation_score"],
            100.0
        )

        self.assertEqual(
            result[1]["recommendation_score"],
            40.0
        )

    def test_cooking_time_filter(self):
        result = recommend_recipes(
            ["egg", "cheese"],
            max_cooking_time=10,
            recipes=self.recipes
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test Omelette")

    def test_empty_recipe_list(self):
        result = recommend_recipes(
            ["egg"],
            recipes=[]
        )

        self.assertEqual(result, [])

    def test_ai_enabled(self):
        result = recommend_recipes(
            ["egg", "cheese"],
            recipes=self.recipes,
            use_ai=True
        )

        self.assertTrue(len(result) > 0)

        for recipe in result:
            self.assertIn("ai_score", recipe)
            self.assertIn("recommendation_score", recipe)

    def test_ai_disabled(self):
        result = recommend_recipes(
            ["egg", "cheese"],
            recipes=self.recipes,
            use_ai=False
        )

        self.assertTrue(len(result) > 0)

        for recipe in result:
            self.assertEqual(recipe["ai_score"], 0)


if __name__ == "__main__":
    unittest.main()
