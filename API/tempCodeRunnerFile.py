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
            if enlaces_resultados == []:
                return jsonify({"resultados": enlaces_resultados})

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