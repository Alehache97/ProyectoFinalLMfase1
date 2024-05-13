import os
import requests

# Solicitar al usuario que ingrese el ID de la temporada y el límite de resultados
season_id = input("Introduce el ID de la temporada en formato AAAA-MM (comienza en 2022-10) hasta la actual: ")
result_limit = int(input("Introduce el límite de resultados (máximo 1000): "))

# Verificar que el season_id y el result_limit sean válidos
if len(season_id) != 7 or season_id[4] != '-' or not season_id[:4].isdigit() or not season_id[5:].isdigit():
    print("El formato del ID de temporada debe ser AAAA-MM, comienza en, 2022-10.")
elif result_limit < 1 or result_limit > 1000:
    print("El límite de resultados debe estar entre 1 y 1000.")
else:
    # Recupera el token de la variable de entorno
    api_token = os.environ['CR']
    headers = {'Authorization': f'Bearer {api_token}'}

    # Formatear correctamente la URL para asegurar que el season_id y el límite son tratados como cadenas
    url = f"https://api.clashroyale.com/v1/locations/global/pathoflegend/{season_id}/rankings/players?limit={result_limit}"
    response = requests.get(url, headers=headers)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        rankings = response.json().get('items', [])
        if not rankings:
            print("No se encontraron datos de ranking para la temporada.")
        else:
            print(f"Ranking de jugadores para la temporada {season_id}:")
            for player in rankings:
                name = player['name']
                tag = player['tag']
                rank = player['rank']
                elo_rating = player['eloRating']
                exp_level = player['expLevel']
                clan_info = f"Clan: {player['clan']['name']} ({player['clan']['tag']})" if 'clan' in player else "Sin clan"
                print(f"Rank {rank}: {name} (Tag: {tag}), Nivel: {exp_level}, Raiting: {elo_rating}, {clan_info}")
    elif response.status_code == 404:
        print("No hay ranking disponible para la temporada indicada.")
    else:
        print(f'Error {response.status_code}: {response.json()}')

