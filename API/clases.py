# clases.py
import openai
import requests
from models import db, Historial

class APIOpenAI:
    def obtener_puntos_clave(self, texto, tipo):
        openai.api_key = ""
        if tipo == "tallerista":
            texto = "Necesito saber que profesión puede tener una persona encargada para dirigir la siguiente actividad: " + texto + ". Cuando lo encuentres escribe el siguiente formato: {profesión} en Chile. En caso de que lo escrito no tenga un sentido lógico o no tenga relación con un taller, escribe el siguiente mensaje: Texto inválido."
        elif tipo == "insumos":
            texto = "Necesito saber que insumos serán necesarios para realizar la siguiente actividad: " + texto + ", escribe solo (nada extra) una lista de 5 objetos con el formato 1- comprar objeto \n, asi sucesivamente, en caso de que lo escrito no tenga un sentido lógico o no tenga relación con un taller, escribe el siguiente mensaje: texto invalido"
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
        api_key = ""
        search_engine_id = ''
        if tipo == "tallerista":
            lugares_busqueda = "site:superprof.cl OR site:linkedin.com/in"
            url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}{lugares_busqueda}&cr=Cl&gl=cl'

        elif tipo == "insumos":
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
        if "INVÁLIDO" in query.upper():
            return []
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
            return resultados_por_insumo
        
    def vaciar_base_de_datos(self):
        try:
            db.session.query(Historial).delete()
            db.session.commit()

            return "Base de datos vaciada exitosamente."
        except Exception as e:
            return f'Ocurrió un error al vaciar la base de datos: {str(e)}'