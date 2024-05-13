import os
import requests

# Recupera el token de la variable de entorno
api_token = os.environ['CR']
headers = {'Authorization': f'Bearer {api_token}'}

# Solicitar al usuario que ingrese el tag del jugador
player_tag_input = input("Introduce el tag del jugador sin la almohadilla (#): ")
# Asegurar que el tag está correctamente formateado para la URL
player_tag = f'%23{player_tag_input}'

# Realiza la solicitud a la API para obtener la información del jugador
response_player = requests.get(f'https://api.clashroyale.com/v1/players/{player_tag}', headers=headers)
if response_player.status_code == 200:
    player_data = response_player.json()
    print('Información del jugador:')
    print(f'Nombre: {player_data["name"]}')
    print(f'Nivel: {player_data["expLevel"]}')
    print(f'Trofeos: {player_data["trophies"]}')
    print(f'Trofeos máximos alcanzados: {player_data["bestTrophies"]}')
    print(f'Victorias/derrotas: {player_data["wins"]} / {player_data["losses"]}')
    print(f'Victorias de tres coronas: {player_data["threeCrownWins"]}')
    print(f'Cantidad de batallas: {player_data["battleCount"]}')
    print(f'Total donaciones: {player_data["totalDonations"]}')
    print(f'Victorias en días de guerra: {player_data["warDayWins"]}')
    print(f'Cartas coleccionadas en el clan: {player_data["clanCardsCollected"]}')
    clan_name = player_data.get("clan", {}).get("name", "Sin clan")
    print(f'Clan: {clan_name}')
elif response_player.status_code == 404:
    print('El jugador especificado no existe.')
else:
    print(f'Error {response_player.status_code}: {response_player.json().get("reason", "No se pudo obtener la información")}')

# Realiza la solicitud a la API para obtener los próximos cofres del jugador
response_chests = requests.get(f'https://api.clashroyale.com/v1/players/{player_tag}/upcomingchests', headers=headers)
if response_chests.status_code == 200:
    chests_data = response_chests.json()['items']
    print('Próximos cofres:')
    for i, chest in enumerate(chests_data, 1):
        print(f'{i}. {chest["name"]}')
elif response_chests.status_code == 404:
    print('El jugador especificado no existe.')
else:
    print(f'Error {response_chests.status_code}: {response_chests.json().get("reason", "No se pudo obtener la información de los cofres")}')


#2YC88YRR9