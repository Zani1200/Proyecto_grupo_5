import json

from modelos.modelo_generativo import ModeloGenerativo


class GeneradorTextos:
    def __init__(self):
        self.modelos = []

    def agregar_modelo(self, modelo):
        """Agrega un modelo generativo al sistema."""
        if isinstance(modelo, ModeloGenerativo):
            self.modelos.append(modelo)
        else:
            raise TypeError("El modelo debe ser una instancia de ModeloGenerativo.")

    def generar(self, peticionUsuario: json):
        """Generar texto basado en una plantilla y variables."""
        try:
            valores = json.loads(peticionUsuario)
            variables = {}

            for clave, valor in valores.items():
                if isinstance(valor, dict):
                    for subClave, subValor in valor.items():
                        variables[subClave] = subValor
                else:
                    variables[clave] = valor

            # Extraer variables
            peticion_usuario = valores.get("peticion_usuario", "")
            estado_emocional = valores.get("estado_emocional", "")
            nivel_energia = valores.get("nivel_energia", "")
            ciudad = valores.get("ubicacion", {}).get("ciudad", "desconocida")
            pais = valores.get("ubicacion", {}).get("pais", "desconocido")
            temperatura = valores.get("tiempo", {}).get("temperatura", "desconocida")
            condicion = valores.get("tiempo", {}).get("condición", "desconocida")
            hora_local = valores.get("hora_local", "")

            # Construir el prompt
            plantilla = (
                f"Eres un experto en crear planes personalizados. "
                f"El usuario quiere: {peticion_usuario}. "
                f"Estado emocional: {estado_emocional}. "
                f"Nivel de energía: {nivel_energia}. "
                f"Ubicación: {ciudad}, {pais}. "
                f"Clima: {temperatura}, {condicion}. "
                f"Hora local: {hora_local}. "
                "Genera un plan conciso (máximo 80 palabras) teniendo en cuenta todas las variables. "
                "Piensa paso a paso y sugiere la actividad más popular para el día de hoy."
            )

            resultados = ""
            for modelo in self.modelos:
                try:
                    prompt = modelo.formatear_prompt(plantilla, variables)
                    print("Prompt enviado a OpenAI:", prompt)  # Debug
                    texto_generado = modelo.generar_texto(prompt)
                    if texto_generado:
                        resultados = texto_generado
                        break  # Usar el primer modelo que genere texto
                    else:
                        print("⚠️ El modelo no generó una respuesta válida.")
                except Exception as e:
                    print(f"Error en el modelo {modelo.nombre}: {e}")
                    return f"❌ Error al generar el plan: {e}"

            return resultados if resultados else "No se pudo generar el plan."

        except Exception as e:
            print(f"Error general en GeneradorTextos: {e}")
            return f"❌ Error crítico: {e}"