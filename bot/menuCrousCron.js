const { Client, GatewayIntentBits } = require('discord.js');
const { bartholdiRoleId, vaurouzeRoleId, token, channelId } = require('./config.json');

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once('ready', async () => {
    console.log(`Logged in as ${client.user.tag}`);
    
    const channel = client.channels.cache.get(channelId);
    const fetch = (await import('node-fetch')).default;
    
    if (!channel) {
        console.error('Canal non trouvé.');
        client.destroy(); // Détruire le client si le canal n'est pas trouvé
        return;
    }

    const restaurants = [
        { name: 'vaurouze', role: `<@&${vaurouzeRoleId}>` },
        { name: 'bartholdi', role: `<@&${bartholdiRoleId}>` }
    ];

    try {
        for (const restaurant of restaurants) {
            const response = await fetch(`http://localhost:5000/get-menu?restaurant=${restaurant.name}`);
            
            if (!response.ok) {
                await channel.send(`Erreur lors de la récupération du menu pour ${restaurant.name}.`);
                continue;
            }

            const menuData = await response.json();

            if (menuData.error) {
                await channel.send(`${restaurant.role} API response: ${menuData.error}`);
                continue;
            }

            const dejeuner = menuData.dejeuner[0];
            const starters = dejeuner.menu[0].starter;
            const mainCourses = dejeuner.menu[0].main_courses;
            const desserts = dejeuner.menu[0].dessert;
            const date = dejeuner.date;
            const restaurantName = menuData.nom_ru;

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

            await channel.send(message);
        }
    } catch (error) {
        console.error(error);
        await channel.send('Une erreur est survenue en essayant de récupérer le menu.');
    }

    client.destroy(); // Détruire le client après l'envoi des messages
});

client.login(token); // Utiliser le token du fichier de configuration
