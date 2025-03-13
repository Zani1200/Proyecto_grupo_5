import json
import requests
import streamlit as st

from modelos.modelo_generativo import ModeloGenerativo

BASE_URL = "http://localhost:8001"

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
            peticion_usuario = valores.get("peticion_usuario")
            estado_emocional = valores.get("estado_emocional")
            nivel_energia = valores.get("nivel_energia")
            ciudad = valores.get("ubicacion").get("ciudad")
            pais = valores.get("ubicacion").get("pais")
            temperatura = valores.get("tiempo").get("temperatura")
            condicion = valores.get("tiempo").get("condición")
            hora_local = valores.get("hora_local")

            # Construir el prompt
            plantilla = (
                f"Eres un experto en crear planes personalizados. "
                f"El usuario quiere: {peticion_usuario}. "
                f"Estado emocional: {estado_emocional}. "
                f"Nivel de energía: {nivel_energia}. "
                f"Ubicación: {ciudad}, {pais}. "
                f"Clima: {temperatura}, {condicion}. "
                f"Hora local: {hora_local}. "
                "Genera un plan detallado (mínimo 3 actividades) para que el usuario pueda divertirse. "
                "Incluye lugares específicos y actividades emocionantes. "
                "Además, incluye las coordenadas geográficas (latitud, longitud) de cada lugar recomendado en el siguiente formato interno: "
                "[COORDENADAS: latitud, longitud]. "
                "No muestres las coordenadas en el texto del plan."

            )

            resultados = ""
            for modelo in self.modelos:
                try:
                    prompt = modelo.formatear_prompt(plantilla, variables)
                    print("Prompt enviado a OpenAI:", prompt)  # Debug
                    texto_generado = modelo.generar_texto(prompt)
                    if texto_generado:
                        resultados = texto_generado
                        response = requests.post(f"{BASE_URL}/pregunta_respuesta/insertar", json={
                            "id_usuario": st.session_state.usuario["id"],
                            "pregunta": prompt,
                            "respuesta": resultados,
                            "variables": variables
                        })
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