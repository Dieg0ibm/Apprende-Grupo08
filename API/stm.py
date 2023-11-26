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

if buscar_tallerista:
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
