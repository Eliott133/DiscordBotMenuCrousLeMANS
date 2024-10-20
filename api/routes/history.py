from flask import jsonify
import os
import json

def getAllMenuHistory():
    json_file_path = os.path.join('history', 'menu.json')

    try:
        if not os.path.exists(json_file_path):
            return jsonify({"error": "The file : menu.json doesn't exist"}), 404

        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            menu_history = json.load(json_file)

        return jsonify(menu_history), 200

    except Exception as e:
        return jsonify({"error": f"Erreur lors de la lecture du fichier: {str(e)}"}), 500

