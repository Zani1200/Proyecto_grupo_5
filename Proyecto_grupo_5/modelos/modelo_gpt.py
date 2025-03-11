import openai
from database.base_datos_Supabase import BaseDatos
from modelos.modelo_generativo import ModeloGenerativo


class ModeloGPT(ModeloGenerativo):
    def __init__(self, nombre, version, api_key):
        super().__init__(nombre, version)
        self.api_key = api_key
        openai.api_key = self.api_key
        self.baseDatos = BaseDatos()

    def generar_texto(self, prompt, **kwargs):
        """Genera texto utilizando GPT-4 basado en el prompt proporcionado."""
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en generar planes personalizados para viajeros."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=900
            )
            texto_generado = response.choices[0].message.content
            self.baseDatos.guarda_peticion_AI(prompt, texto_generado, response.model, response.usage.total_tokens, None)
            return texto_generado
        except Exception as e:
            print(f"Error en OpenAI: {e}")
            return None

    def obtener_respuesta(self, plantilla, variables):
        """
        Implementación del método abstracto de ModeloGenerativo.
        Obtiene la respuesta generada usando el formato de la plantilla y las variables.
        """
        try:
            prompt = self.formatear_prompt(plantilla, variables)
            return self.generar_texto(prompt)
        except Exception as e:
            print(f"Error en obtener_respuesta: {e}")
            return None