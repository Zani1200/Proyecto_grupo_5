class ModeloGenerativo:

    def __init__(self, nombre, version):
        self._nombre = nombre
        self._version = version

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, valor):
        self._version = valor

    def cargar_modelo(self):
        # Código para cargar el modelo
        pass

    def generar_texto(self, prompt):
        # Código para generar texto basado en el prompt
        pass

    def limpiar_prompt(self, prompt):
        prompt = prompt.strip()  # Eliminar espacios en blanco al inicio y al final
        prompt = prompt.capitalize()  # Capitalizar la primera letra
        # Añadir más operaciones de limpieza si es necesario
        return prompt

    def formatear_prompt(self, plantilla, variables):
        try:
            prompt_formateado = plantilla.format(**variables)
            return prompt_formateado
        except KeyError as e:
            print(f"Error: Falta la variable {e} en el diccionario de variables.")
            return plantilla