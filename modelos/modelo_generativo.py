from abc import ABC, abstractmethod

class ModeloGenerativo(ABC):
    """ Clase base abstracta para modelos generativos """

    def __init__(self, nombre, version):
        self._nombre = nombre
        self._version = version

    @abstractmethod
    def obtener_respuesta(self, plantilla, variables):
        """ Método abstracto para generar texto con IA """
        pass

    @property
    def nombre(self):
        return self._nombre

    @property
    def version(self):
        return self._version

    def cargar_modelo(self):
        """ Método común para cargar el modelo, a implementar por las subclases. """
        pass

    def generar_texto(self, prompt):
        """ Método para generar texto a partir de un prompt. A implementar por las subclases. """
        pass

    def limpiar_prompt(self, prompt):
        """ Método para limpiar el prompt. """
        return prompt.strip()  # Eliminar espacios en blanco al inicio y al final

    def formatear_prompt(self, plantilla, variables):
        """ Método para formatear el prompt con las variables. """
        try:
            return plantilla.format(**variables)
        except KeyError as e:
            print(f"Error: Falta la variable {e} en el diccionario de variables.")
            return plantilla  # Retorna la plantilla original si hay un error
