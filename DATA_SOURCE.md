# Recipe Dataset - Data Source Documentation

## 1. Dataset Overview

The AI Recipe Recommender project uses a manually created recipe dataset.

The dataset contains 20 sample recipes designed for testing and demonstrating the recipe recommendation system.

## 2. Data Source

The recipes were manually created by the project team.

No external recipe dataset or third-party API was used to create the current sample dataset.

The dataset is intended for educational and project demonstration purposes.

## 3. Dataset Structure

Each recipe contains the following fields:

| Field | Description |
|---|---|
| name | Name of the recipe |
| ingredients | List of required ingredients |
| instructions | Preparation instructions |
| cooking_time | Cooking time in minutes |
| category | Recipe category |
| servings | Number of servings |

## 4. Data Format

The dataset is stored in JSON format.

File name: `recipes.json`

Each recipe is represented as a JSON object inside a list.

## 5. Data Cleaning

The `data_processing.py` module is responsible for loading, validating, and cleaning recipe data.

The data processing operations include:

- Removing recipes with missing or invalid information.
- Converting ingredient names to lowercase.
- Removing unnecessary spaces.
- Removing duplicate ingredients within a recipe.
- Validating cooking time and serving information.
- Checking that each recipe contains valid ingredients.

## 6. Dataset Statistics

- Total recipes: 20
- Valid recipes: 20
- Invalid recipes: 0
- Language: English
- Format: JSON

## 7. Dataset Limitations

The current dataset contains a limited number of manually created sample recipes.

It is intended for testing and demonstration, not as a comprehensive collection of real-world recipes.

The dataset can be expanded with additional recipes in future development.