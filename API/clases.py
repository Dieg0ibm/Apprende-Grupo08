# clases.py
import openai
import requests
from models import db, Historial

class APIOpenAI:
    def obtener_puntos_clave(self, texto, tipo):
<<<<<<< HEAD
        openai.api_key =""     #1 clave
=======
        openai.api_key ="sk-proj-nNdbhlD61jGxUeKA0QFjT3BlbkFJUYjFkInNYV2iC8Caqwpy"     #1 clave
>>>>>>> dd45d54 (Hito 3(Nueva HU, y tests))
        if tipo == "tallerista":
            texto = "Necesito saber que profesión puede tener una persona encargada para dirigir la siguiente actividad: " + texto + ". Cuando lo encuentres escribe el siguiente formato: {profesión} en Chile."
        elif tipo == "insumos":
            texto = "Necesito saber que insumos serán necesarios para realizar la siguiente actividad: " + texto + ", escribe solo (nada extra) una lista de 5 objetos con el formato 1- comprar objeto \n, asi sucesivamente"
        respuesta = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=texto,
            max_tokens=100,
            n=1,
        )
        puntos_clave = [eleccion['text'] for eleccion in respuesta.choices]
        return puntos_clave

class APIGoogleCustomSearch:
    def realizar_busqueda(self, query, tipo):
<<<<<<< HEAD
        api_key = ""
        search_engine_id = ''                     #Ocultamos key porque el repositorio es público
=======
        api_key = "AIzaSyCQluKUBI9QNnZkH61ALj9XMu0jWFNGJb4"
        search_engine_id = 'b39aece0cb9b74cd3'                     #Ocultamos key porque el repositorio es público
>>>>>>> dd45d54 (Hito 3(Nueva HU, y tests))
        if tipo == "tallerista":
            lugares_busqueda = "site:superprof.cl OR site:linkedin.com/in"
            url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}{lugares_busqueda}&cr=Cl&gl=cl'

        elif tipo == "insumos":
            lugares_busqueda = "site:amazon.com"
            url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}'
    
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            enlaces = [item['link'] for item in data.get('items', [])]
            return enlaces
        else:
            print('Error en la solicitud a Google Custom Search:', response.status_code)
            return []

class UsuarioApprende:
    def __init__(self, nombre, contacto):
        self.nombre = nombre
        self.contacto = contacto

    def ingresar_necesidad(self, descripcion_taller, api_openai, api_custom_search, tipo):
        puntos_clave = api_openai.obtener_puntos_clave(descripcion_taller, tipo)
        query = " ".join(puntos_clave)
        print(query)
        
        if tipo == "tallerista":
            enlaces = api_custom_search.realizar_busqueda(query, tipo)
            return enlaces
        elif tipo == "insumos":
            lineas = query.split('\n')
            resultados_por_insumo = {}

            for i, linea in enumerate(lineas):
                if linea and len(linea)>3:
                    enlaces = api_custom_search.realizar_busqueda(linea, tipo)
                    resultados_por_insumo[linea] = enlaces[:1]

            print(resultados_por_insumo)
            return resultados_por_insumo
        
    def vaciar_base_de_datos(self):
        try:
            db.session.query(Historial).delete()
            db.session.commit()

            return "Base de datos vaciada exitosamente."
        except Exception as e:
            return f'Ocurrió un error al vaciar la base de datos: {str(e)}'