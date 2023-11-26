#app.py
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from clases import UsuarioApprende, APIOpenAI, APIGoogleCustomSearch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)

openai_api = APIOpenAI()
custom_search_api = APIGoogleCustomSearch()

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_miembro = db.Column(db.String(255))
    contacto_miembro = db.Column(db.String(255))
    descripcion_taller = db.Column(db.String(255))
    tipo = db.Column(db.String(50))
    enlaces_resultados = db.Column(db.Text)

class Search(Resource):
    def post(self):
        try:
            data = request.get_json()
            nombre_miembro = data.get('nombre_miembro')
            contacto_miembro = data.get('contacto_miembro')
            descripcion_taller = data.get('descripcion_taller')
            tipo = data.get('tipo')

            usuario = UsuarioApprende("Vicente", "vicente.romero@usm.cl")
            enlaces_resultados = usuario.ingresar_necesidad(descripcion_taller, openai_api, custom_search_api, tipo)

            if not enlaces_resultados:
                return jsonify({"mensaje": f"No se encontraron resultados de {tipo}."}), 404

            nuevo_registro = Historial(
                nombre_miembro=nombre_miembro,
                contacto_miembro=contacto_miembro,
                descripcion_taller=descripcion_taller,
                tipo=tipo,
                enlaces_resultados='\n'.join(enlaces_resultados)
            )

            db.session.add(nuevo_registro)
            db.session.commit()
            print("Nuevo registro guardado en el historial:", nuevo_registro)

            return jsonify({"resultados": enlaces_resultados})
        except Exception as e:
            print(f"Error en la búsqueda: {str(e)}")
            return jsonify({'error': 'Ocurrió un error durante la búsqueda.'}), 500

api.add_resource(Search, '/search')

class Resultados(Resource):
    def post(self):
        try:
            data = request.get_json()
            resultados = data.get('resultados', [])
            return jsonify({"resultados": resultados})
        except Exception as e:
            print(f"Error al procesar los resultados: {str(e)}")
            return jsonify({'error': 'Ocurrió un error al procesar los resultados.'}), 500

api.add_resource(Resultados, '/resultados')

class HistorialResource(Resource):
    def get(self):
        try:
            historial = Historial.query.all()
            historial_data = [{
                'id': registro.id,
                'nombre_miembro': registro.nombre_miembro,
                'contacto_miembro': registro.contacto_miembro,
                'descripcion_taller': registro.descripcion_taller,
                'tipo': registro.tipo,
                'enlaces_resultados': registro.enlaces_resultados
            } for registro in historial]

            return jsonify({"historial": historial_data})
        except Exception as e:
            print(f"Error al obtener el historial: {str(e)}")
            return jsonify({'error': 'Ocurrió un error al obtener el historial.'}), 500

api.add_resource(HistorialResource, '/historial')

def vaciar_base_de_datos():
    try:
        db.session.query(Historial).delete()
        db.session.commit()

        return "Base de datos vaciada exitosamente."
    except Exception as e:
        return f'Ocurrió un error al vaciar la base de datos: {str(e)}'

class BorrarHistorial(Resource):
    def get(self):
        try:
            resultado = vaciar_base_de_datos()  # Llama a la función directamente
            return jsonify({"resultado": resultado})
        except Exception as e:
            print(f"Error al intentar borrar el historial: {str(e)}")
            return jsonify({'error': 'Ocurrió un error al intentar borrar el historial.'}), 500

api.add_resource(BorrarHistorial, '/borrar_historial')

@app.route('/')
def index():
    return '¡Bienvenido a la aplicación de búsqueda!'

@app.route('/favicon.ico')
def favicon():
    return 'Favicon no encontrado'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)