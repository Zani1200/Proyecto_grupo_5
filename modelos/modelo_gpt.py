from modelos.modelo_generativo import ModeloGenerativo
import openai
import os


class ModeloGPT(ModeloGenerativo):
    def __init__(self, nombre, version, api_key):
        super().__init__(nombre, version)
        self.api_key = api_key
        openai.api_key = self.api_key  # Configurar la clave de la API

    def generar_texto(self, prompt, **kwargs):
        try:
            # ✅ NUEVO FORMATO para openai.ChatCompletion
            response = openai.chat.completions.create(
                model="gpt-4",  # Asegura que el modelo sea correcto
                messages=[
                    {"role": "system", "content": "eres un experto en crear planes de viajes"},
                    {"role": "user", "content": prompt}],  # Formato actualizado
                # max_tokens=150,
                temperature=0.7,
                **kwargs  # Permite opciones adicionales
            )

            # ✅ Extraer el contenido correctamente
            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Ocurrió un error al generar el texto: {e}")
            return None

    def obtener_respuesta(self, plantilla, variables):
        """ Obtiene la respuesta generada usando el formato de la plantilla y las variables. """
        prompt_formateado = self.formatear_prompt(plantilla, variables)
        return self.generar_texto(prompt_formateado)

    def formatear_prompt(self, plantilla, variables):
        """ Formatea el prompt con las variables pasadas, limpiando las variables. """
        # Limpiar las variables para asegurarse de que no hay espacios extra
        variables = {k.strip(): v.strip() for k, v in variables.items()}  # Eliminar espacios extra
        prompt = plantilla.format(**variables)  # Formatear el prompt con las variables
        return prompt

    def limpiar_prompt(self, prompt):
        """ Limpia el prompt convirtiéndolo a minúsculas y eliminando espacios extra. """
        return prompt.strip().lower()
