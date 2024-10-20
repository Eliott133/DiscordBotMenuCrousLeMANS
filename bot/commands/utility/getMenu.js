const { SlashCommandBuilder } = require('discord.js');
const { bartholdiRoleId, vaurouzeRoleId } = require('../../config.json');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('getmenu')
        .setDescription('Affiche le menu du jour pour Vaurouze et Bartholdi.'),

    async execute(interaction) {
        try {
            // Utiliser l'import dynamique pour charger node-fetch
            const fetch = (await import('node-fetch')).default;

            // Liste des restaurants et des rôles associés
            const restaurants = [
                { name: 'vaurouze', role: `<@&${vaurouzeRoleId}>` }, // ID du rôle Discord pour Vaurouze
                { name: 'bartholdi', role: `<@&${bartholdiRoleId}>` } // ID du rôle Discord pour Bartholdi
            ];

            // Répondre d'abord à l'interaction
            await interaction.reply('Récupération des menus...');
            
            // Boucler sur les restaurants et fetch les menus
            for (const restaurant of restaurants) {
                // Fetch les données depuis ton API pour chaque restaurant
                const response = await fetch(`http://localhost:5000/get-menu?restaurant=${restaurant.name}`);
                
                if (!response.ok) {
                    await interaction.followUp(`Erreur lors de la récupération du menu pour ${restaurant.name}.`);
                    continue; // Passer au prochain restaurant
                }

                // Récupérer et parser le JSON
                const menuData = await response.json();

                // Vérifier si l'API renvoie une erreur
                if (menuData.error) {
                    await interaction.followUp(`${restaurant.role} API response: ${menuData.error}`);
                    continue;
                }

                // Extraire les sections du menu
                const dejeuner = menuData.dejeuner[0]; // Le menu de déjeuner du premier jour
                const starters = dejeuner.menu[0].starter;
                const mainCourses = dejeuner.menu[0].main_courses;
                const desserts = dejeuner.menu[0].dessert;
                const date = dejeuner.date;
                const restaurantName = menuData.nom_ru;

                // Construire le message à afficher avec la mention du rôle
                let message = `${restaurant.role} **${restaurantName} - ${date}**\n\n`;

                message += '**Entrées :**\n';
                starters.forEach(starter => {
                    message += `- ${starter}\n`;
                });

                message += '\n**Plats principaux :**\n';
                mainCourses.forEach(mainCourse => {
                    message += `- ${mainCourse}\n`;
                });

                message += '\n**Desserts :**\n';
                desserts.forEach(dessert => {
                    message += `- ${dessert}\n`;
                });

                // Envoyer un message pour chaque restaurant
                await interaction.followUp(message);
            }

            // Supprimer le message de récupération des menus
            await interaction.deleteReply();

        } catch (error) {
            console.error(error);
            await interaction.followUp('Une erreur est survenue en essayant de récupérer le menu.');
        }
    }
};
