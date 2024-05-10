#app.py

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import db, Historial, Propuestas
from clases import APIOpenAI, APIGoogleCustomSearch, UsuarioApprende

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)

openai_api = APIOpenAI()
custom_search_api = APIGoogleCustomSearch()

@app.route('/propuesta_taller', methods=['POST'])
def recibir_propuesta():
    data = request.get_json()

    # Verificar si algún atributo está vacío
    if any(value == "" or value is None for value in data.values()):
        return jsonify({"error": "La propuesta de taller no cumple con el formato esperado."})
    
    nueva_propuesta = Propuestas(
        nombre_miembro=data['nombre_miembro'],
        contacto_miembro=data['contacto_miembro'],
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        duracion=data['duracion'],
        sesiones=data['sesiones'],
        objetivos=data['objetivos'],
        estado=data['estado']
    )

    db.session.add(nueva_propuesta)
    db.session.commit()
    return jsonify({"propuesta": data})


@app.route('/propuestas', methods=['GET'])
def get_propuestas():
    propuestas = Propuestas.query.all()
    propuestas_data = [{
        'id': propuesta.id,
        'nombre_miembro': propuesta.nombre_miembro,
        'contacto_miembro': propuesta.contacto_miembro,
        'titulo': propuesta.titulo,
        'descripcion': propuesta.descripcion,
        'duracion': propuesta.duracion,
        'sesiones': propuesta.sesiones,
        'objetivos': propuesta.objetivos,
        'estado':propuesta.estado
    } for propuesta in propuestas]
    return jsonify({"propuestas": propuestas_data})

class Search(Resource):
    def post(self):
        try:
            data = request.get_json()
            nombre_miembro = data.get('nombre_miembro')
            contacto_miembro = data.get('contacto_miembro')
            descripcion_taller = data.get('descripcion_taller')
            tipo = data.get('tipo')

            usuario = UsuarioApprende(nombre_miembro, contacto_miembro)
            enlaces_resultados = usuario.ingresar_necesidad(descripcion_taller, openai_api, custom_search_api, tipo)
            print(enlaces_resultados)

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

class BorrarPropuesta(Resource):
    def delete(self, propuesta_id):
        try:
            propuesta = Propuestas.query.get(propuesta_id)
            if not propuesta:
                return jsonify({"error": "La propuesta no existe."}), 404

            db.session.delete(propuesta)
            db.session.commit()
            return jsonify({"mensaje": "Propuesta eliminada correctamente."})
        except Exception as e:
            print(f"Error al eliminar la propuesta: {str(e)}")
            return jsonify({'error': 'Ocurrió un error al eliminar la propuesta.'}), 500

api.add_resource(BorrarPropuesta, '/propuestas/<int:propuesta_id>')

@app.route('/propuestas/<int:propuesta_id>', methods=['PUT'])
def actualizar_estado_propuesta(propuesta_id):
    try:
        data = request.get_json()
        nuevo_estado = data.get('estado')
        
        if nuevo_estado is None:
            return jsonify({"error": "Se requiere el parámetro 'estado' para actualizar la propuesta."}), 400
        
        # Obtener la propuesta por su ID
        propuesta = Propuestas.query.get(propuesta_id)
        
        if not propuesta:
            return jsonify({"error": "La propuesta no existe."}), 404
        
        # Actualizar el estado de la propuesta
        propuesta.estado = nuevo_estado
        db.session.commit()
        
        return jsonify({"mensaje": "Estado de propuesta actualizado correctamente."}), 200
    
    except Exception as e:
        print(f"Error al actualizar la propuesta: {str(e)}")
        return jsonify({'error': 'Ocurrió un error al actualizar la propuesta.'}), 500
    


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