import os
import time
from interfaces.generador_textos import GeneradorTextos
from interfaces.Presentacion import Presentacion
from modelos.modelo_gpt import ModeloGPT
from database.usuarios import Usuario


def main():
    # Obtener la API Key de OpenAI desde la variable de entorno

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ Error: No se ha encontrado la API Key de OpenAI en las variables de entorno.")
        return
    # Instancio un usuario de prueba
    usuario = Usuario("example", "example@gmail.com", "example")

    """ Función principal del programa """
    # puse asi la api_key porque no me iba con el "os.getenv("OPENAI_API_KEY")" pero ya se cambiara

    modelo_gpt = ModeloGPT("GPT-4", "v1.0", openai_api_key)

    # Crear instancia de Presentacion
    presentacion = Presentacion(modelo_gpt)

    # Crear instancia del generador de textos
    generador = GeneradorTextos()
    generador.agregar_modelo(modelo_gpt)

    while True:
        # Mostrar menú usando Presentacion.py
        opcion = presentacion.mostrar_menu()

        if opcion == "1":
            presentacion.plan_adaptado(generador)
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
