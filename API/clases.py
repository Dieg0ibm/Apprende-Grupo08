# clases.py
import openai
import requests
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_miembro = db.Column(db.String(255))
    contacto_miembro = db.Column(db.String(255))
    descripcion_taller = db.Column(db.String(255))
    tipo = db.Column(db.String(50))
    enlaces_resultados = db.Column(db.Text)

class APIOpenAI:
    def obtener_puntos_clave(self, texto, tipo):
        openai.api_key = ""
        if tipo == "tallerista":
            texto = "Necesito saber que profesión puede tener una persona encargada para dirigir la siguiente actividad: " + texto + ". Cuando lo encuentres escribe el siguiente formato: {profesión} en Chile."
        elif tipo == "insumos":
            texto = "Necesito saber que insumos serán necesarios para realizar la siguiente actividad: " + texto + ", escribe una lista de 5 objetos con el formato 1- comprar objeto \n, asi sucesivamente"
        respuesta = openai.Completion.create(
            engine="text-davinci-003",
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
        print(query)
        
        if tipo == "tallerista":
            enlaces = api_custom_search.realizar_busqueda(query, tipo)
            return enlaces
        elif tipo == "insumos":
            lineas = query.split('\n')
            resultados_por_insumo = {}

            for i, linea in enumerate(lineas):
                if linea:
                    enlaces = api_custom_search.realizar_busqueda(linea, tipo)
                    resultados_por_insumo[linea] = enlaces[:2]

            print(resultados_por_insumo)
            return resultados_por_insumo
        
    def vaciar_base_de_datos(self):
        try:
            db.session.query(Historial).delete()
            db.session.commit()

            return "Base de datos vaciada exitosamente."
        except Exception as e:
            return f'Ocurrió un error al vaciar la base de datos: {str(e)}'