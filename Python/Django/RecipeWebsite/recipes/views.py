# RecipeWebsite/recipes/views.py

from django.shortcuts import render, get_object_or_404
from .models import Meal
import requests

def get_countries_and_races():
    countries_response = requests.get('https://restcountries.com/v2/all')
    countries_data = countries_response.json()

    country_to_race = {}
    for country_info in countries_data:
        country_name = country_info.get('name', '').lower()
        race_name = country_info.get('demonym', '').lower()
        country_to_race[country_name] = race_name

    return country_to_race

COUNTRY_TO_RACE = get_countries_and_races()

def convert_country_name(country_name):
    converted_name = COUNTRY_TO_RACE.get(country_name.lower(), country_name.lower())
    return converted_name

def home(request):
    countries_response = requests.get('https://restcountries.com/v2/all')
    countries = sorted(countries_response.json(), key=lambda x: x['name'])

    error_message = ""
    selected_meal_id = None
    selected_meal = None
    image_url = None

    if request.method == 'POST':
        selected_country = request.POST.get('country')
        selected_meal_name = request.POST.get('meal')

        if selected_country:
            selected_country = convert_country_name(selected_country)

            meals_response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?a={selected_country}')
            meals_data = meals_response.json()

            if meals_data['meals'] is not None:
                meals = meals_data['meals']
                selected_meal_id = next((meal['idMeal'] for meal in meals if meal['strMeal'] == selected_meal_name), None)

                if selected_meal_id:
                    meal_detail_response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={selected_meal_id}')
                    meal_detail_data = meal_detail_response.json()
                    selected_meal = meal_detail_data['meals'][0]
                    selected_meal['ingredients'] = get_ingredients(selected_meal)

                    # Food photos with Pixabay API
                    pixabay_api_key = 'YOUR_KEY'

                    try:
                        # Filter irrelevant photos with additional parameters
                        pixabay_url = f'https://pixabay.com/api/?key={pixabay_api_key}&q={selected_meal["strMeal"]}&image_type=photo&lang=en&min_width=800&min_height=600'
                        pixabay_response = requests.get(pixabay_url)
                        pixabay_data = pixabay_response.json()
                        image_url = pixabay_data['hits'][0]['largeImageURL'] if pixabay_data['hits'] else None
                    except Exception as e:
                        image_url = None
                        print(f"Error fetching image from Pixabay: {e}")
                else:
                    error_message = f"Meal ID not found for {selected_meal_name}."
            else:
                meals = []
                error_message = f"No meals found for {selected_country}."
        else:
            meals = []
            error_message = "Please select a country."

    else:
        selected_country = None
        meals = []
        error_message = ""

    return render(request, 'recipes/home.html', {'countries': countries, 'selected_country': selected_country, 'meals': meals, 'selected_meal': selected_meal, 'image_url': image_url, 'error_message': error_message})

def get_ingredients(meal):
    ingredients = []
    for i in range(1, 21):
        ingredient_key = f'strIngredient{i}'
        measure_key = f'strMeasure{i}'
        ingredient = meal.get(ingredient_key)
        measure = meal.get(measure_key)
        if ingredient and measure:
            ingredients.append(f"{ingredient} - {measure}")
    return ingredients
