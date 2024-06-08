import unittest
import requests

##################################################################################################################################

class PropuestaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://127.0.0.1:5000'
        cls.propuesta_form_valida_data = {
            'nombre_miembro': 'Vicente Romero',
            'contacto_miembro': 'vicente.romero@usm.cl',
            'titulo': 'Taller de Rugby para principiantes',
            'descripcion': 'Deseo hacer un taller de rugby donde la gente que asista sean gente interesada en el deporte y que nunca haya tenido contacto con este.',
            'duracion': 80,
            'sesiones': 3,
            'objetivos': 'Fomentar la práctica de rugby, Promover el deporte en general',
            'estado': 0  # Estado inicial
        }

        cls.propuesta_form_invalida_data = {
            'nombre_miembro': 'Claudio Varela',
            'contacto_miembro': 'c.varela@usm.cl',
            'titulo': 'Taller de futbol',
            'descripcion': '',  ### dato vacío por lo tanto es una propuesta inválida
            'duracion': 70,
            'sesiones': 3,
            'objetivos': 'Fomentar la práctica del futbol , Promover el deporte en adultos',
            'estado': 0  # Estado inicial
        }

    @classmethod
    def tearDownClass(cls):
        del cls.propuesta_form_valida_data
        del cls.propuesta_form_invalida_data

    def test_creacion_propuesta_taller_valida(self):
        url = f'{self.base_url}/propuesta_taller'
        response = requests.post(url, json=self.propuesta_form_valida_data)
        response_data = response.json()

        # Verificar si la respuesta tiene el atributo "propuesta"
        self.assertIn("propuesta", response_data)

        if "propuesta" in response_data:
            # Obtener el cuerpo de la respuesta JSON
            response_body = response_data["propuesta"]

            # Verificar todos los atributos de la propuesta
            propuesta_valida = (
                response_body["nombre_miembro"] != "" and
                response_body["contacto_miembro"] != "" and
                response_body["titulo"] != "" and
                response_body["descripcion"] != "" and
                isinstance(response_body["duracion"], int) and
                isinstance(response_body["sesiones"], int) and
                response_body["objetivos"] != "" and
                isinstance(response_body["estado"], int)
            )

            # Asegurarse de que todos los atributos de la propuesta sean válidos
            self.assertTrue(propuesta_valida, "La propuesta de taller no cumple con los atributos esperados.")
    
    def test_creacion_propuesta_taller_invalida(self):
        url = f'{self.base_url}/propuesta_taller'
        response = requests.post(url, json=self.propuesta_form_invalida_data)
        response_data = response.json()

        # Verificar si la respuesta tiene el atributo "error"
        self.assertIn("error", response_data)

        if "error" in response_data:
        # Verificar el mensaje de error recibido
            error_message = response_data["error"]
            expected_error_message = "La propuesta de taller no cumple con el formato esperado."

            # Asegurarse de que el mensaje de error es el esperado
            self.assertEqual(error_message, expected_error_message, "Mensaje de error incorrecto.")

##################################################################################################################################

class BusquedaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://127.0.0.1:5000'
        cls.busqueda_valida = {
            'descripcion': "Quiero realizar un taller de salud mental",
            'tipo': 'tallerista'
        }
        cls.busqueda_invalida = {
            'descripcion': "adasdsadsadsadasdsadsdsa",
            'tipo': 'tallerista'
        }

    @classmethod
    def tearDownClass(cls):
        del cls.busqueda_valida
        del cls.busqueda_invalida

    def test_busqueda_valida(self):
        url = f'{self.base_url}/search'
        response = requests.post(url, json={'descripcion_taller': self.busqueda_valida['descripcion'], 'tipo': self.busqueda_valida['tipo']})
        response_data = response.json()

        # Verificar si la respuesta tiene el atributo "resultados"
        self.assertIn("resultados", response_data)

        if "resultados" in response_data:
            # Verificar si los resultados no están vacíos
            resultados = response_data["resultados"]
            self.assertTrue(resultados, "La búsqueda no devolvió resultados.")

    def test_busqueda_invalida(self):
        url = f'{self.base_url}/search'
        response = requests.post(url, json={'descripcion_taller': self.busqueda_invalida['descripcion'], 'tipo': self.busqueda_invalida['tipo']})
        response_data = response.json()
        self.assertIn("resultados", response_data)
        print(response_data)
        # Verificar si la clave "resultados" está en los datos de respuesta
        if "resultados" in response_data:
            resultados = response_data["resultados"]
            # Verificar si los resultados están vacíos
            self.assertFalse(resultados, "La búsqueda debería devolver resultados vacíos.")
        else:
            print("La clave 'resultados' no se encontró en los datos de respuesta.")


if __name__ == '__main__':
    unittest.main()
