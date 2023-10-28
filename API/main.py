import openai
import requests

openai.api_key = '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'

def obtener_puntos_clave(texto):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=texto,
        max_tokens=100,  # Ajusta el número de tokens según tu preferencia
        n=1,  # Número de puntos clave que deseas obtener
    )

    puntos_clave = [eleccion['text'] for eleccion in respuesta.choices]
    return puntos_clave

flag = True

while flag:
    texto = "quiero que extraigas la necesidad del siguiente texto, simplemente lo que necesita no quiero el para o porque: "
    texto += input("Ingresar su necesidad: ")
    puntos_clave = obtener_puntos_clave(texto)

    query = " ".join(puntos_clave)
    print(query)

    # Define la URL de la API de Google Custom Search
    api_key = "AIzaSyBmNVHpXXBxK7cHWopWGKCx632HN3as3M4"
    search_engine_id = 'b39aece0cb9b74cd3'

    # Define la lista de sitios web donde deseas buscar
    lugares_busqueda = "site:linkedin.com OR site:superprof.cl"

    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query} {lugares_busqueda}&cr=Cl'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("\nHemos encontrado lo siguiente: ")
        # resultados de la búsqueda de Google Custom Search
        for item in data.get('items', []):
            title = item['title']
            link = item['link']
            print("")
            print(f'Título: {title}')
            print(f'Enlace: {link}')
    else:
        print('Error en la solicitud a Google Custom Search:', response.status_code)

    print("")
    eleccion = input("Ingrese 1 si desea continuar: ")
    if eleccion!="1":
        flag = False
    else:
        print("")

