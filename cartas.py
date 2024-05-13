import os
import requests

# Recupera el token de la variable de entorno
api_token = os.environ['CR']

# Configura los encabezados de autorización
headers = {
    'Authorization': f'Bearer {api_token}'
}

# Realiza la solicitud a la API para obtener todas las cartas
response = requests.get('https://api.clashroyale.com/v1/cards', headers=headers)

# Verifica si la solicitud fue exitosa
if response.status_code == 200:
    cards_data = response.json()['items']
    
    # Pide el nombre (o parte del nombre) de la carta que se desea buscar
    search_term = input("Ingresa el nombre o parte inicial de la carta que deseas buscar: ").strip().lower()

    # Inicializa una lista vacía para las cartas encontradas
    found_cards = []

    # Recorre cada carta en la lista `cards_data`
    for card in cards_data:
        # Comprueba si el nombre comienza con el término buscado, ignorando mayúsculas/minúsculas
        if card['name'].strip().lower().startswith(search_term):
            # Si coincide, añade la carta a la lista de cartas encontradas
            found_cards.append(card)

    # Comprueba si la lista de cartas encontradas no está vacía
    if found_cards:
        # Recorre las cartas encontradas para imprimir sus datos
        for card in found_cards:
            print(f'Nombre: {card["name"]}')
            print(f'Elixir: {card["elixirCost"]}')
            print(f'Rareza: {card["rarity"]}')
            print(f'ID: {card["id"]}')
            print(f'Icono: {card["iconUrls"]["medium"]}')
            print('---')
    else:
        # Si no se encontraron cartas, muestra un mensaje indicándolo
        print('No se encontró ninguna carta que comience con ese nombre.')
else:
    print(f'Error {response.status_code}: {response.json()}')