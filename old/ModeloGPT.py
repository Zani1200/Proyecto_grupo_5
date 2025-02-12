from Proyecto_Grupo_5.ModeloGenerativo import ModeloGenerativo

class ModeloGPT(ModeloGenerativo):
    def __init__(self, nombre, version, api_key):
        super().__init__(nombre, version)
        self.api_key = api_key

    def generar_texto(self, prompt):
        # Implementación específica para GPT
        # Por ejemplo, realizar una llamada a la API de OpenAI
        texto_generado = f"Texto generado por {self.nombre} versión {self.version} para el prompt: {prompt}"
        return texto_generado

    def generar_texto(self, plantilla, variables):
        prompt_formateado = self.formatear_prompt(plantilla, variables)
        prompt_limpio = self.limpiar_prompt(prompt_formateado)
        # Implementación específica para GPT utilizando prompt_limpio
        texto_generado = f"Texto generado por {self.nombre} versión {self.version} para el prompt: {prompt_limpio}"
        return texto_generado

modelo_gpt = ModeloGPT("GPT-4", "v1.0", "tu_api_key")
prompt_usuario = " escRibe un poema sobre la inteLigencia artificial  "
prompt_limpio = modelo_gpt.limpiar_prompt(prompt_usuario)
print(f"Prompt limpio: '{prompt_limpio}'")

plantilla = "Escribe un artículo sobre {tema} que incluya {punto_clave}."
variables = {
    "tema": "la inteligencia artificial en la educación",
    "punto_clave": "los beneficios de personalizar el aprendizaje"
}

texto = modelo_gpt.generar_texto(plantilla, variables)
print("El texto a partir de la plantilla es:", texto)