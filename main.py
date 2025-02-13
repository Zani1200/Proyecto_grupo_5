import os
import time
from interfaces.generador_textos import GeneradorTextos
from interfaces.Presentacion import Presentacion
from modelos.modelo_gpt import ModeloGPT


def main():
    """ Función principal del programa """

    # Crear instancia de Presentacion
    presentacion = Presentacion(ModeloGPT)

    # Crear instancia del generador de textos
    generador = GeneradorTextos()

    # Obtener la API Key de OpenAI desde la variable de entorno
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ Error: No se ha encontrado la API Key de OpenAI en las variables de entorno.")
        return

    # Crear instancia del Modelo GPT y agregarlo al generador
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", openai_api_key)
    generador.agregar_modelo(modelo_gpt)

    while True:
        # Mostrar menú usando Presentacion.py
        opcion = presentacion.mostrar_menu()

        if opcion == "1":
            presentacion.plan_adaptado()
        elif opcion == "2":
            presentacion.solicitar_experiencia()
        elif opcion == "3":
            presentacion.ver_base_datos()
        elif opcion == "4":
            presentacion.mostrarDespedida()
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

        input("\n🔄 Presiona ENTER para continuar...")  # Espera antes de volver al menú


if __name__ == "__main__":
    main()
