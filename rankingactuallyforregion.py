import os
import requests

# Solicita al usuario que ingrese el nombre de una región
input_region = input("Introduce el nombre de la región: ")
region_name = input_region.capitalize()

# Recupera el token de la variable de entorno
api_token = os.environ['CR']
headers = {'Authorization': f'Bearer {api_token}'}

# Asigna None a location_id e is_country
location_id = None
is_country = None

# Manejo de la opción "Global" o búsqueda de una región específica
if region_name == "Global":
    location_id = 'global'
else:
    url_locations = "https://api.clashroyale.com/v1/locations"
    response_locations = requests.get(url_locations, headers=headers)
    if response_locations.status_code == 200:
        locations = response_locations.json().get('items', [])
        found = False
        for location in locations:
            if location['name'].capitalize() == region_name and not found:
                location_id = location['id']
                is_country = location['isCountry']
                found = True

# Solicitar el límite de resultados dentro del rango permitido
result_limit = int(input("Introduce el límite de resultados (1-1000), si el número de rankeados en la región indicada es inferior al número indicado se mostrarán todos los rankeados de dicha región: "))

if not found:
    print("No se encontró una región o país con ese nombre.")
if result_limit < 1 or result_limit > 1000:
    print("El límite de resultados debe estar entre 1 y 1000.")

if location_id and (is_country is not False or location_id == 'global'):
    url_ranking = f"https://api.clashroyale.com/v1/locations/{location_id}/pathoflegend/players?limit={result_limit}"
    response_ranking = requests.get(url_ranking, headers=headers)
    if response_ranking.status_code == 200:
        rankings = response_ranking.json().get('items', [])
        if rankings:
            print(f"Ranking de jugadores para la región {region_name}:")
            for player in rankings:
                name = player['name']
                tag = player['tag']
                rank = player['rank']
                elo_rating = player.get('eloRating', 'No disponible')
                exp_level = player['expLevel']
                clan_info = f"Clan: {player['clan']['name']} ({player['clan']['tag']})" if 'clan' in player else "Sin clan"
                print(f"Rank {rank}: {name} (Tag: {tag}), Nivel: {exp_level}, Puntuación: {elo_rating}, {clan_info}")
        else:
            print("No se encontraron datos de ranking para la región especificada.")
    else:
        print("No se pudo obtener el ranking para la región.")
elif location_id and is_country is False:
    print("Has ingresado el nombre de un continente. Por favor, indica el nombre de un país o 'global' para ver el ranking global.")
else:
    print("Por favor, ingresa una opción válida para la región.")
