import requests
from flask import jsonify
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime, timedelta
import locale
import json
import os

def get_menu(url, date_str):
    # Effectuer la requête GET
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": f"Erreur lors de la récupération des données sur le site du crous : {response.status_code}"}

    # Analyser le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupérer le nom du restaurant
    nom_ru = soup.find("h1", class_="post_title").text.strip()

    # Initialiser un dictionnaire pour le nouveau déjeuner
    meal_data = {
        "date": date_str,
        "menu": []
    }

    # Récupérer les dates de menu
    menu_dates = soup.find_all("time", class_="menu_date_title")

    # Indicateur pour savoir si nous avons déjà trouvé le menu pour la date
    found_menu = False

    # Parcourir les dates de menu
    for date_tag in menu_dates:
        menu_date = date_tag.text.strip()

        if menu_date == date_str and not found_menu:  # Vérifier si la date correspond et qu'aucun menu n'est trouvé
            # 3. Récupérer les sections 'meal' liées à cette date
            meals = date_tag.find_next("div", class_="meal")

            # 4. Parcourir les 'meal' et trouver celui dont le titre est 'Déjeuner'
            if meals:
                title = meals.find_next("div", class_="meal_title")
                
                if title and title.text.strip() == "Déjeuner":
                    # 5. Récupérer la liste des éléments sous 'meal_foodies' pour le déjeuner
                    meal_foodies = meals.find_next("ul", class_="meal_foodies")
                    
                    if meal_foodies:
                        entries = []
                        main_courses = []
                        desserts = []

                        # Parcourir les sections de nourriture
                        food_categories = meal_foodies.find_all("li")
                        for category in food_categories:
                            category_title = category.contents[0].strip()  # Titre de la catégorie (RU Entrées, etc.)
                            food_items = category.find_all("li")

                            # Assigner les plats selon la catégorie
                            if "Entrées" in category_title or "ENTREES" in category_title:
                                entries = [item.text.strip() for item in food_items]
                            elif "Plats" in category_title:
                                main_courses = [item.text.strip() for item in food_items]
                            elif "Desserts" in category_title or "Dessert" in category_title:
                                desserts = [item.text.strip() for item in food_items]

                        # Construire le menu
                        meal_data["menu"].append({
                            "starter": entries,
                            "main_courses": main_courses,
                            "dessert": desserts
                        })

            # Une fois le menu trouvé, on évite d'ajouter plusieurs fois pour la même date
            found_menu = True
            return {
                "nom_ru": nom_ru,
                "dejeuner": [meal_data]  # Encapsuler le déjeuner dans une liste
            }

    return {"error": "Not menu today"}