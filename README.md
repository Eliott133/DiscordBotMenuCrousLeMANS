# DiscordBotMenuCrousLeMANS

**DiscordBotMenuCrousLeMANS** is a Discord bot that allows users to view the daily menu of the CROUS du [Mans](https://maps.app.goo.gl/vVjcftFnFu1uCN838) directly on their Discord server. The bot interacts with a Flask API to retrieve menu data and display it in a user-friendly way.

## Features

- Retrieves and displays the menus of the CROUS du Mans.
- Supports multiple restaurants and daily menus.
- Can be configured to send automatic notifications of menus every day.
- Stores the menus in a json file that acts as a database

## Prerequisites

Before you can use the bot, make sure you have the following software installed:

- [Node.js](https://nodejs.org/) (version 14 or higher)
- [Python](https://www.python.org/) (version 3.8 or higher)
- [Discord.js](https://discord.js.org/) to handle the Discord integration
- [Flask](https://flask.palletsprojects.com/) for the backend API

## Installation

### Clone the repository

```bash
git clone https://github.com/Eliott133/DiscordBotMenuCrousLeMANS.git
cd DiscordBotMenuCrousLeMANS
```

### Bot Configuration

1) Create a config.json file at:
```bash
DiscordBotMenuCrousLeMANS/bot/
```
Following the structure of the config.example.json file

2) Install the project dependencies:
```bash
npm install
```

### Flask API Setup

1) Navigate to the ```api``` folder and install the Python dependencies:
```bash
pip install -r requirements.txt
```

2) Launch the Flask API:
```bash
python app.py
```

#### About Flask API

##### Endpoint

This API has three Endpoint:

- **/get-menu** : This endpoint allows you to retrieve the menu of the day for a given restaurant.
- **/save-menu** : This endpoint allows you to save the new menu of the day for a specific restaurant.
- **/get-history-menu** : This endpoint allows you to consult the history of saved menus for a given restaurant. It returns a list of previously saved menus, with the corresponding date.

These routes return a JSON format in response.

## Start the bot

Configure a cron job on your server from Monday to Friday before the menus appear by running this command:
```bash
node bot.js
```

When launching the bot. The bot will search the API for the daily menu for the two CROUS restaurants in LE MANS.
