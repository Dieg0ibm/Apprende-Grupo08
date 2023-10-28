import openai
import requests

class Tallerista:
    def __init__(self, nombre, detalles_contacto):
        self.nombre = nombre
        self.detalles_contacto = detalles_contacto

class APIOpenAI:
    def obtener_puntos_clave(self, texto):
        openai.api_key = ""
        respuesta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=texto,
            max_tokens=100,
            n=1,
        )
        puntos_clave = [eleccion['text'] for eleccion in respuesta.choices]
        return puntos_clave

class APIGoogleCustomSearch:
    def realizar_busqueda(self, query):
        api_key = ""
        search_engine_id = ""
        lugares_busqueda = "site:superprof.cl OR site:linkedin.com"
        url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query} {lugares_busqueda}&cr=Cl&gl=cl'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            perfiles_talleristas = []
            for item in data.get('items', []):
                title = item['title']
                link = item['link']
                tallerista = Tallerista(title, link)
                perfiles_talleristas.append(tallerista)
            return perfiles_talleristas
        else:
            print('Error en la solicitud a Google Custom Search:', response.status_code)
            return []

class UsuarioApprende:
    def __init__(self, nombre, contacto):
        self.nombre = nombre
        self.contacto = contacto

    def ingresar_necesidad(self, descripcion_taller, api_openai, api_custom_search):
        puntos_clave = api_openai.obtener_puntos_clave(descripcion_taller)
        query = " ".join(puntos_clave)
        perfiles_talleristas = api_custom_search.realizar_busqueda(query)
        return perfiles_talleristas

class Programa:
    def __init__(self, api_openai, api_custom_search):
        self.api_openai = api_openai
        self.api_custom_search = api_custom_search

    def mostrarResultados(self, usuario, descripcion_taller):
        perfiles_talleristas = usuario.ingresar_necesidad(descripcion_taller, self.api_openai, self.api_custom_search)
        if not perfiles_talleristas:
            print("No se encontraron resultados de talleristas.")
        else:
            print("Hemos encontrado lo siguiente: ")
            for tallerista in perfiles_talleristas:
                print("")
                print(f'Nombre: {tallerista.nombre}')
                print(f'Detalles de Contacto: {tallerista.detalles_contacto}')

flag = True
nombre_miembro = input("Ingrese su nombre: ")
contacto_miembro = input("Ingrese sus detalles de contacto: ")
api_openai = APIOpenAI()
api_custom_search = APIGoogleCustomSearch()

while flag:
    usuario = UsuarioApprende(nombre_miembro, contacto_miembro)
    programa = Programa(api_openai, api_custom_search)
    descripcion_taller = "quiero que extraigas la necesidad del siguiente texto, simplemente lo que necesita no quiero el para o porque: "
    descripcion_taller += input("Ingresar la descripción del taller: ")
    programa.mostrarResultados(usuario, descripcion_taller)

    print("")
    eleccion = input("Ingrese 1 si desea continuar: ")
    if eleccion != "1":
        flag = False
    else:
        print("")
