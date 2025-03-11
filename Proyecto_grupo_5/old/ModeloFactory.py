from Proyecto_Grupo_5.ModeloGPT import ModeloGPT

class ModeloFactory:
    @staticmethod
    def crear_modelo(tipo, nombre, version, **kwargs):
        if tipo == "GPT":
            return ModeloGPT(nombre, version, kwargs.get("api_key"))
        elif tipo == "OtroModelo":
            # Implementar otras subclases si existen
            pass
        else:
            raise ValueError(f"Tipo de modelo '{tipo}' no reconocido.")

modelo_gpt = ModeloFactory.crear_modelo(
    tipo="GPT",
    nombre="GPT-4",
    version="v2.0",
    api_key="tu_api_key"
)

print("Modelo de modeloFactory:", modelo_gpt.nombre)  # Debería imprimir: GPT-4