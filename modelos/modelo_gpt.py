from modelos.modelo_generativo import ModeloGenerativo
import openai
from database.base_datos_Supabase import BaseDatos


class ModeloGPT(ModeloGenerativo):
    def __init__(self, nombre, version, api_key):
        super().__init__(nombre, version)
        self.api_key = api_key
        openai.api_key = self.api_key  # Configurar la clave de la API
        self.baseDatos = BaseDatos()

    def generar_texto(self, prompt, **kwargs):
        try:
            # ✅ NUEVO FORMATO para openai.ChatCompletion
            response = openai.chat.completions.create(
                model="gpt-4",  # Asegura que el modelo sea correcto
                messages=[
                    {"role": "system", "content": """1. Eres un experto en crear planes
                    2. A partir de los datos que te entreguen debes de generar el plan ideal para el usuario
                    3. la respuesta debe ser concisa teniendo en cuenta todas las variables
                    4. ten en cuenta todas las actividades que se pueden realizar el día de hoy y decide la más popular
                    5. que no posea más de 80 palabras
                    6. piensa paso a paso"""},
                    {"role": "user", "content": prompt}],  # Formato actualizado
                # max_tokens=150,
                temperature=0.7,
                **kwargs  # Permite opciones adicionales
            )
            # ✅ Extraer el contenido correctamente
            self.baseDatos.guarda_peticion_AI(prompt, response.choices[0].message.content, response.model, response.usage.total_tokens,None)
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
