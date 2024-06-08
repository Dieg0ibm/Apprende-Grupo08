import requests
import streamlit as st
from models import Historial, Propuestas

# Configuración de la página
st.set_page_config(
    page_title="Apprende",
    page_icon="logo.png",
    layout="wide",
)

st.image("logo.png", width=150)

# Crear las pestañas
tabs = ["Buscar Tallerista", "Buscar Insumo", "Ver Historial", "Enviar Propuesta", "Propuestas Pendientes", "Propuestas Aprobadas"]
selected_tab = st.sidebar.selectbox("Selecciona una opción", tabs)

if selected_tab == "Buscar Tallerista":
    st.title("Buscar Tallerista")
    descripcion_taller = st.text_area("Descripción del Taller")
    buscar_tallerista = st.button("Buscar Tallerista")
    
    if buscar_tallerista:
        if not descripcion_taller:
            st.warning("Por favor, ingresa una descripción del taller antes de realizar la búsqueda.")
        else:
            with st.spinner("Realizando búsqueda de tallerista..."):
                try:
                    response = requests.post('http://127.0.0.1:5000/search', json={'descripcion_taller': descripcion_taller, 'tipo': 'tallerista'})
                    response.raise_for_status()
                    resultados = response.json().get("resultados", [])

                    if resultados:
                        st.header("Resultados de Talleristas: ")
                        response_resultados = requests.post('http://127.0.0.1:5000/resultados', json={'resultados': resultados})
                        response_resultados.raise_for_status()

                        resultados_organizados = response_resultados.json().get("resultados", [])
                        st.write(resultados_organizados)
                        if resultados_organizados == []:
                            st.error("CHAP")
                        for enlace in resultados_organizados:
                            st.write(enlace)
                    else:
                        st.error("No se encontraron resultados de tallerista.")
                except requests.RequestException as e:
                    st.error(f"Error al realizar la solicitud: {e}")

elif selected_tab == "Buscar Insumo":
    st.title("Buscar Insumo")
    descripcion_taller = st.text_area("Descripción del Taller")
    buscar_insumo = st.button("Buscar Insumo")
    
    if buscar_insumo:
        if not descripcion_taller:
            st.warning("Por favor, ingresa una descripción del taller antes de realizar la búsqueda.")
        else:
            with st.spinner("Realizando búsqueda de insumo..."):
                try:
                    response = requests.post('http://127.0.0.1:5000/search', json={'descripcion_taller': descripcion_taller, 'tipo': 'insumos'})
                    response.raise_for_status()

                    resultados = response.json().get("resultados", [])

                    if resultados:
                        st.write("Para realizar el siguiente taller te recomendamos comprar: ")
                        for objeto, enlaces in resultados.items():
                            st.write(objeto)
                            for enlace in enlaces:
                                st.write(enlace)
                    else:
                        st.error("No se encontraron resultados de insumo.")
                except requests.RequestException as e:
                    st.error(f"Error al realizar la solicitud: {e}")

elif selected_tab == "Ver Historial":
    st.title("Ver Historial")
    ver_historial = st.button("Ver Historial")
    
    if ver_historial:
        st.header("Historial")
        with st.spinner("Cargando historial..."):
            try:
                response_historial = requests.get('http://127.0.0.1:5000/historial')
                response_historial.raise_for_status()

                historial = response_historial.json().get("historial", [])
                if historial:
                    for registro in historial:
                        st.write(f"Descripción Taller: {registro['descripcion_taller']}")
                        st.write(f"Tipo: Búsqueda de {registro['tipo']}")
                        
                        if registro['tipo']=="tallerista":
                            st.write("Enlaces:")
                        elif registro['tipo']=="insumos":
                            st.write("Productos")
                        enlaces = registro['enlaces_resultados'].split("\n")
                        for enlace in enlaces:
                            st.write(enlace)

                        st.write("-" * 50)
                else:
                    st.error("No hay registros en el historial.")
                
            except requests.RequestException as e:
                st.error(f"Error al realizar la solicitud: {e}")

elif selected_tab == "Enviar Propuesta":
    st.title("Enviar Propuesta de Taller")
    with st.form("formulario_taller"):
        nombre_miembro = st.text_input("Nombre del Miembro")
        contacto_miembro = st.text_input("Contacto del Miembro")
        titulo = st.text_input("Título del evento")
        descripcion = st.text_input("Descripción del taller")
        duracion = st.number_input("Duración aproximada en minutos", min_value=1)  
        sesiones = st.number_input("Número de sesiones", min_value=1)  
        objetivos =  st.text_area("Objetivos")
        enviar_propuesta = st.form_submit_button("Enviar Propuesta")
        estado = 0
    if enviar_propuesta:
        if not nombre_miembro or not contacto_miembro or not titulo or not descripcion or not duracion or not sesiones or not objetivos:
            st.warning("Por favor, completa todos los campos antes de enviar la propuesta.")
        else:
            with st.spinner("Enviando propuesta de taller..."):
                try:
                    data = {
                        "nombre_miembro": nombre_miembro,
                        "contacto_miembro": contacto_miembro,
                        "titulo": titulo,
                        "descripcion": descripcion,
                        "duracion": duracion,
                        "sesiones": sesiones,
                        "objetivos": objetivos,
                        "estado": estado
                    }
                    response = requests.post('http://127.0.0.1:5000/propuesta_taller', json=data)
                    if response.status_code == 200:
                        st.success("Propuesta de taller enviada correctamente.")
                    else:
                        st.error("Error al enviar la propuesta de taller.")
                except requests.RequestException as e:
                    st.error(f"Error al enviar la propuesta: {e}")

elif selected_tab == "Propuestas Pendientes":
    st.title("Propuestas Pendientes de Taller")
    response_propuestas = requests.get('http://127.0.0.1:5000/propuestas?estado=0')  # Filtrar por estado pendiente
    if response_propuestas.status_code == 200:
        propuestas_pendientes = [propuesta for propuesta in response_propuestas.json().get("propuestas", []) if propuesta['estado'] == 0]
        if propuestas_pendientes:
            st.header("Propuestas Pendientes de Taller")
            # Código para mostrar propuestas y menú desplegable
            titulos_propuestas = [propuesta['titulo'] for propuesta in propuestas_pendientes]
            propuesta_seleccionada = st.selectbox("Selecciona una propuesta para ver:", titulos_propuestas)
            # Obtener los detalles de la propuesta seleccionada
            propuesta_elegida = next((propuesta for propuesta in propuestas_pendientes if propuesta['titulo'] == propuesta_seleccionada), None)
            if propuesta_elegida:
                st.subheader("Detalles de la Propuesta")
                st.write(f"Título: {propuesta_elegida['titulo']}")
                st.write(f"Nombre del Miembro: {propuesta_elegida['nombre_miembro']}")
                st.write(f"Contacto del Miembro: {propuesta_elegida['contacto_miembro']}")
                st.write(f"Descripción: {propuesta_elegida['descripcion']}")
                st.write(f"Duración: {propuesta_elegida['duracion']} minutos")
                st.write(f"Sesiones: {propuesta_elegida['sesiones']}")
                st.write(f"Objetivos:")
                st.write(propuesta_elegida['objetivos'])
                
                # Mostrar estado de la propuesta
                estado_propuesta = "Pendiente" if propuesta_elegida['estado'] == 0 else "Aprobada"
                st.write(f"Estado: {estado_propuesta}")
                # Opciones para eliminar y aprobar la propuesta
                col1, col2 = st.columns(2)
                if col1.button("Eliminar Propuesta"):
                    propuesta_id = propuesta_elegida['id']
                    response_eliminar = requests.delete(f'http://127.0.0.1:5000/propuestas/{propuesta_id}')
                    if response_eliminar.status_code == 200:
                        st.success("Propuesta eliminada correctamente.")
                    else:
                        st.error("Error al eliminar la propuesta.")
                if col2.button("Aprobar Propuesta"):
                    propuesta_id = propuesta_elegida['id']
                    response_aprobar = requests.put(f'http://127.0.0.1:5000/propuestas/{propuesta_id}', json={"estado": 1})
                    if response_aprobar.status_code == 200:
                        st.success("Propuesta aprobada correctamente.")
                    else:
                        st.error("Error al aprobar la propuesta.")
            else:
                st.warning("No se encontraron detalles de la propuesta seleccionada.")
        else:
            st.warning("No hay propuestas pendientes.")
    else:
        st.error("Error al obtener las propuestas pendientes.")


elif selected_tab == "Propuestas Aprobadas":
    st.title("Propuestas Aprobadas de Taller")
    response_propuestas = requests.get('http://127.0.0.1:5000/propuestas?estado=1')  # Filtrar por estado pendiente
    if response_propuestas.status_code == 200:
        propuestas_pendientes = [propuesta for propuesta in response_propuestas.json().get("propuestas", []) if propuesta['estado'] == 1]
        if propuestas_pendientes:
            st.header("Propuestas Pendientes de Taller")
            # Código para mostrar propuestas y menú desplegable
            titulos_propuestas = [propuesta['titulo'] for propuesta in propuestas_pendientes]
            propuesta_seleccionada = st.selectbox("Selecciona una propuesta para ver:", titulos_propuestas)
            # Obtener los detalles de la propuesta seleccionada
            propuesta_elegida = next((propuesta for propuesta in propuestas_pendientes if propuesta['titulo'] == propuesta_seleccionada), None)
            if propuesta_elegida:
                st.subheader("Detalles de la Propuesta")
                st.write(f"Título: {propuesta_elegida['titulo']}")
                st.write(f"Nombre del Miembro: {propuesta_elegida['nombre_miembro']}")
                st.write(f"Contacto del Miembro: {propuesta_elegida['contacto_miembro']}")
                st.write(f"Descripción: {propuesta_elegida['descripcion']}")
                st.write(f"Duración: {propuesta_elegida['duracion']} minutos")
                st.write(f"Sesiones: {propuesta_elegida['sesiones']}")
                st.write(f"Objetivos:")
                st.write(propuesta_elegida['objetivos'])
                
                # Mostrar estado de la propuesta
                estado_propuesta = "Pendiente" if propuesta_elegida['estado'] == 0 else "Aprobada"
                st.write(f"Estado: {estado_propuesta}")
                # Opciones para eliminar y aprobar la propuesta
                col1, col2 = st.columns(2)
                if col1.button("Eliminar Propuesta"):
                    propuesta_id = propuesta_elegida['id']
                    response_eliminar = requests.delete(f'http://127.0.0.1:5000/propuestas/{propuesta_id}')
                    if response_eliminar.status_code == 200:
                        st.success("Propuesta eliminada correctamente.")
                    else:
                        st.error("Error al eliminar la propuesta.")
                if col2.button("Enviar nuevamente a revisión"):
                    propuesta_id = propuesta_elegida['id']
                    response_aprobar = requests.put(f'http://127.0.0.1:5000/propuestas/{propuesta_id}', json={"estado": 0})
                    if response_aprobar.status_code == 200:
                        st.success("Propuesta aprobada correctamente.")
                    else:
                        st.error("Error al aprobar la propuesta.")
            else:
                st.warning("No se encontraron detalles de la propuesta seleccionada.")
        else:
            st.warning("No hay propuestas pendientes.")
    else:
        st.error("Error al obtener las propuestas pendientes.")