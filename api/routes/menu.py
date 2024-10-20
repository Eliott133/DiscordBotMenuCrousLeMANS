from flask import request, jsonify
from datetime import datetime, timedelta
import locale
from utils.menu_scraper import get_menu
import os
import json

RESTAURANTS = {"bartholdi": "https://www.crous-nantes.fr/restaurant/resto-u-bartholdi/",
               "vaurouze": "https://www.crous-nantes.fr/restaurant/resto-u-vaurouze/"}

locale.setlocale(locale.LC_ALL, 'French_France')

def menu_endpoint():
    restaurant = request.args.get('restaurant')

    if not restaurant:
        return jsonify({"error": "The param 'restaurant' is required"}), 400

    today = datetime.now().strftime("Menu du %A %d %B %Y")
    hier = datetime.now() + timedelta(days=1)
    yesterday_str = hier.strftime("Menu du %A %d %B %Y")

    if restaurant in RESTAURANTS:
        url = RESTAURANTS[restaurant]
        menu = get_menu(url, today)

        if not menu:
            return jsonify({"error": "Menu not found or not available"}), 404

        if "error" in menu:
            return menu
        
        return jsonify(menu), 200
    else:
        available_restaurants = list(RESTAURANTS.keys())
        return jsonify({
            "error": f"The restaurant '{restaurant}' doesn't exist.",
            "available_restaurants": available_restaurants
        }), 404
    
def save_menu():
    restaurant = request.args.get('restaurant')

    if not restaurant:
        return jsonify({"error": "The param 'restaurant' is required"}), 500

    locale.setlocale(locale.LC_ALL, 'French_France')

    today = datetime.now().strftime("Menu du %A %d %B %Y")
    hier = datetime.now() - timedelta(days=2)
    yesterday_str = hier.strftime("Menu du %A %d %B %Y")

    if restaurant in RESTAURANTS:
        url = RESTAURANTS[restaurant]
        menu = get_menu(url, yesterday_str)

        if not menu:
            return jsonify({"error": "Menu not found or not available"}), 404

        if "error" in menu:
            return menu
        
        json_file_path = os.path.join('history', 'menu.json')
        
        if not os.path.exists(json_file_path):
            # Si le fichier n'existe pas, initialiser une structure JSON vide
            all_menus = []
        else:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                all_menus = json.load(json_file)

        menu_date = menu['dejeuner'][0]['date']  # Récupérer la date du menu
        nom_ru = menu['nom_ru']  # Récupérer le nom du restaurant

        # Vérifier si le restaurant est déjà dans la liste
        for existing_menu in all_menus:
            if existing_menu['nom_ru'] == nom_ru:
                # Si le menu de la date existe déjà, ne pas l'ajouter
                if any(m['date'] == menu_date for m in existing_menu['dejeuner']):
                    return jsonify(
                        {"error": "Menu for this date already saved", 
                        "information": "Check history menu at this endpoint : '/get-history-menu"}), 400
                existing_menu['dejeuner'].insert(0, {
                    "date": menu_date,
                    "menu": menu['dejeuner'][0]['menu']
                })
                break
        else:
            # Ajouter un nouveau restaurant
            all_menus.insert(0, {
                "nom_ru": nom_ru,
                "dejeuner": [{
                    "date": menu_date,
                    "menu": menu['dejeuner'][0]['menu']
                }]
            })
        
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_menus, json_file, ensure_ascii=False, indent=4)
        
        return jsonify(menu, {"succes": "The menu has been saved"}), 200
    else:
        available_restaurants = list(RESTAURANTS.keys())
        return jsonify({
            "error": f"The restaurant '{restaurant}' doesn't exist.",
            "available_restaurants": available_restaurants
        }), 404
