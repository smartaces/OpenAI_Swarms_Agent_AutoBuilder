"""
Functions for the cocktail_maker agent
"""
import sys
import os
# Add the parent directory to the Python path
sys.path.append('/content/swarm/examples/magic')
from base.memory_manager import memory_manager
from agents.cocktail_maker.content import cocktail_content
def make_cocktail_recommendation():
    """
    Prompts the user for available ingredients and provides cocktail recipe recommendations using the Free Cocktail API.
    """
    try:
        user_input = input("Please enter the ingredients you have (separated by commas): ")
        if not user_input:
            print("No ingredients provided. Please provide at least one ingredient.")
            return None
        # Process input: split ingredients and remove extra spaces
        ingredients = [ingredient.strip() for ingredient in user_input.split(",") if ingredient.strip()]
        if not ingredients:
            print("No valid ingredients provided.")
            return None
        # Use the first ingredient to perform the API search with the test API key '1'
        import requests
        base_url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="
        ingredient = ingredients[0]
        response = requests.get(base_url + ingredient)
        if response.status_code != 200:
            print("Error contacting cocktail API. Please try again later.")
            return None
        data = response.json()
        if not data or data.get("drinks") is None:
            print(f"No cocktails found containing {ingredient}.")
            return None
        cocktails = [drink.get("strDrink", "Unknown") for drink in data["drinks"]]
        suggestions = cocktails[:5]  # Return up to 5 suggestions
        result_message = f"Based on the ingredient '{ingredient}', here are some cocktail suggestions: {', '.join(suggestions)}"
        print(result_message)
        return suggestions
    except Exception as e:
        print("An error occurred while retrieving cocktail recommendations:", e)
        return None