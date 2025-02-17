import json
import os

from analisis.EnriquecerPeticionUsuario import procesar_peticion
from modelos.modelo_generativo import ModeloGenerativo
from modelos.modelo_gpt import ModeloGPT
from interfaces.Presentacion import Presentacion


class GeneradorTextos:
    def __init__(self):
        self.modelos = []

    def agregar_modelo(self, modelo):
        """ Agrega un modelo generativo al sistema. """
        if isinstance(modelo, ModeloGenerativo):
            self.modelos.append(modelo)
        else:
            raise TypeError("El modelo debe ser una instancia de ModeloGenerativo.")

    def generar(self, peticionUsuario: json):
        """ Generar texto basado en una plantilla y variables. """

        valores = json.loads(peticionUsuario)
        variables = {}

        for clave, valor in valores.items():
            if isinstance(valor, dict):
                for subClave, subValor in valor.items():
                    variables[subClave] = subValor
            else:
                variables[clave] = valor

        peticion_usuario = valores.get("peticion_usuario")
        nivel_energia = valores.get("nivel_energia")
        estado_emocional = valores.get("estado_emocional")
        ciudad = valores.get("localizacion").get("ciudad")
        pais = valores.get("localizacion").get("pais")
        temperatura = valores.get("tiempo").get("temperatura")
        condicion = valores.get("tiempo").get("condición")
        hora_local = valores.get("hora_local")

        plantilla = f"{peticion_usuario} con un nivel de energia {nivel_energia}, su estado emocional es {estado_emocional}, el pais es {pais} en la ciudad {ciudad}, " \
                    f"la temperatura es {temperatura}, su condicion es {condicion} y la hora es {hora_local}"

        resultados = {}

        for modelo in self.modelos:
            try:
                # Formatear el prompt con las variables proporcionadas
                prompt = modelo.formatear_prompt(plantilla, variables)

                # Generar texto con OpenAI
                texto_generado = modelo.generar_texto(prompt)

                if texto_generado:
                    resultados[modelo.nombre] = texto_generado
                else:
                    print(f"⚠️ Advertencia: El modelo '{modelo.nombre}' no generó texto válido.")

            except Exception as e:
                print(f"❌ Error al generar texto con el modelo '{modelo.nombre}': {e}")
        print(resultados)
        return resultados


def mostrar_interfaz():
    """ Muestra la interfaz del programa. """
    presentacion = Presentacion()
    presentacion.mostrarBienvenida()
    print("\n" + "*" * 50)
    presentacion.mostrarMenu()
    print("\n" + "*" * 50)
    presentacion.solicitarInputAlUsuario()
    print("\n" + "*" * 50)
    presentacion.solicitarMasDatosInicial()
    print("\n" + "*" * 50)
    presentacion.solicitarMasDatosSucesivo()
    print("\n" + "*" * 50)
    presentacion.mostrarPlanActividades(presentacion.planDeActividades)
    print("\n" + "*" * 50)
    presentacion.mostrarDespedida()
    print("\n" + "*" * 50)


def main():
    """ Función principal del programa. """
    generador = GeneradorTextos()
    """
    api_key = os.getenv("OPENAI_API_KEY")  # Obtener la clave de API desde variables de entorno

    if not api_key:
        print("❌ ERROR: La API key de OpenAI no está configurada.")
        return
    """

    modelo_gpt = ModeloGPT("GPT-4", "v1.0",
                           api_key="OPENAI_API_KEY")
    generador.agregar_modelo(modelo_gpt)

    entrada_json = json.dumps({
        "peticion_usuario": "Me apetecería darme un buen baño en algún sitio molón.",
        "nivel_energia": "3"
    })

    valoresUsuario = procesar_peticion(entrada_json)
    generador.generar(valoresUsuario)


if __name__ == "__main__":
    "mostrar_interfaz()"
    main()
