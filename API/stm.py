import requests
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Apprende",
    page_icon="logo.png",
    layout="wide",
)

st.image("logo.png", width=150)

st.title("Sistema de Búsqueda Apprende")
descripcion_taller = st.text_area("Descripción del Taller")
st.sidebar.title("Opciones")

buscar_tallerista = st.button("Buscar Tallerista")
buscar_insumo = st.button("Buscar Insumo")
ver_historial = st.sidebar.button("Ver Historial")
borrar_historial = st.sidebar.button("Borrar Historial")
ver_propuestas = st.sidebar.button("Ver Propuestas")  # Botón para ver las propuestas

# streamlit_app.py
import requests
import streamlit as st

# Agregar formulario de propuesta de taller
with st.sidebar.form("formulario_taller"):
    nombre_miembro = st.text_input("Nombre del Miembro")
    contacto_miembro = st.text_input("Contacto del Miembro")
    titulo = st.text_input("Título del evento")
    descripcion = st.text_input("Descripción del taller")
    duracion = st.number_input("Duración aproximada en minutos", min_value=1)  
    sesiones = st.number_input("Número de sesiones", min_value=1)  
    objetivos =  st.text_area("Objetivos")
    enviar_propuesta = st.form_submit_button("Enviar Propuesta")

# Procesar la propuesta de taller cuando se envíe el formulario
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
                    "objetivos": objetivos
                }
                response = requests.post('http://127.0.0.1:5000/propuesta_taller', json=data)

                if response.status_code == 200:
                    st.success("Propuesta de taller enviada correctamente.")
                else:
                    st.error("Error al enviar la propuesta de taller.")
            except requests.RequestException as e:
                st.error(f"Error al enviar la propuesta: {e}")

# Añadir condición para verificar si la descripción del taller está vacía

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

                    for enlace in resultados_organizados:
                        st.write(enlace)
                else:
                    st.error("No se encontraron resultados de tallerista.")
            except requests.RequestException as e:
                st.error(f"Error al realizar la solicitud: {e}")

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

if borrar_historial:
    with st.spinner("Borrando historial..."):
        try:
            response_borrar_historial = requests.get('http://127.0.0.1:5000/borrar_historial')
            response_borrar_historial.raise_for_status()
            st.success(response_borrar_historial.json().get("mensaje", "Historial borrado exitosamente."))
            pass
        except requests.RequestException as e:
            st.error(f"Error al realizar la solicitud: {e}")

# Mostrar las propuestas cuando se presione el botón correspondiente
if ver_propuestas:
    response_propuestas = requests.get('http://127.0.0.1:5000/propuestas')
    if response_propuestas.status_code == 200:
        propuestas = response_propuestas.json().get("propuestas", [])
        if propuestas:
            st.header("Propuestas de Taller")
            st.json(propuestas)  # Imprimir el JSON en Streamlit
        else:
            st.warning("No hay propuestas almacenadas.")
    else:
        st.error("Error al obtener las propuestas.")
