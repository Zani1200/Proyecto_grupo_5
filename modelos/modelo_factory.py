from modelo_gpt import ModeloGPT


class ModeloFactory:
    """Clase Factory para crear instancias de modelos generativos."""

    # Diccionario para registrar los modelos disponibles
    modelos_disponibles = {
        "GPT": ModeloGPT
    }

    @staticmethod
    def crear_modelo(tipo, nombre, version, **kwargs):
        """
        Crea y devuelve una instancia del modelo solicitado.

        :param tipo: Tipo de modelo (por ejemplo, "GPT").
        :param nombre: Nombre del modelo.
        :param version: Versión del modelo.
        :param kwargs: Parámetros adicionales (como api_key para GPT).
        :return: Instancia del modelo solicitado.
        """
        modelo_clase = ModeloFactory.modelos_disponibles.get(tipo)

        if modelo_clase:
            if tipo == "GPT":
                # Para el modelo GPT, necesitamos la API key
                api_key = kwargs.get("api_key")
                if not api_key:
                    raise ValueError("Se requiere una API Key para crear un modelo GPT.")
                return modelo_clase(nombre, version, api_key)
            else:
                # Si agregamos más modelos en el futuro, implementamos aquí la lógica
                raise NotImplementedError(f"El modelo '{tipo}' aún no está implementado.")
        else:
            raise ValueError(f"Tipo de modelo '{tipo}' no reconocido.")