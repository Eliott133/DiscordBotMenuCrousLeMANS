from flask import Flask
from flask_cors import CORS
from routes.menu import menu_endpoint, save_menu
from routes.history import getAllMenuHistory

app = Flask(__name__)
CORS(app)

# Enregistrement des routes depuis les modules séparés
app.add_url_rule('/get-menu', 'menu_endpoint', menu_endpoint, methods=['GET'])
app.add_url_rule('/save-menu', 'save_menu', save_menu, methods=['GET'])
app.add_url_rule('/get-history-menu', 'getAllMenuHistory', getAllMenuHistory, methods=['GET'])

if __name__ == '__main__':
    app.run()
