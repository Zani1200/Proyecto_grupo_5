import os
from interfaces.generador_textos import GeneradorTextos
from interfaces.Presentacion import Presentacion
from modelos.modelo_gpt import ModeloGPT

def mostrar_interfaz():
    # Creación de la instancia de Presentacion
    presentacion = Presentacion()

    # Mostrar la bienvenida
    presentacion.mostrarBienvenida()

    # Mostrar el menú
    print("\n" + "*" * 50)
    presentacion.mostrarMenu()

def main():
    # Crear la instancia del Generador de Textos
    generador = GeneradorTextos()

    # Obtener la API Key de OpenAI desde la variable de entorno
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Verificar que la clave de la API esté configurada correctamente
    if not openai_api_key:
        print("Error: No se ha encontrado la API Key de OpenAI en las variables de entorno.")
        return

    # Crear la instancia del Modelo GPT con la configuración adecuada
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", openai_api_key)

    # Agregar el modelo generativo al generador de textos
    generador.agregar_modelo(modelo_gpt)

    # Crear la instancia de Presentacion para la despedida
    presentacion = Presentacion()

    while True:
        # Mostrar el título
        print("\n" + "*" * 50)
        print("=== Generador de Textos Personalizado ===")

        # Solicitar la plantilla al usuario (Ejemplo: generar experiencia viajera)
        plantilla = input("Ingresa una plantilla de prompt (ejemplo: 'Generar una experiencia viajera para {destino} donde se realizarán actividades de {actividad}.') (o 'salir' para terminar): ")

        # Verificar si el usuario desea salir
        if plantilla.lower() == 'salir':
            break

        # Solicitar el número de variables a ingresar
        num_variables = int(input("¿Cuántas variables deseas ingresar? (ejemplo: destino, actividad): "))

        # Solicitar las variables al usuario y almacenarlas en un diccionario
        variables = {}
        for _ in range(num_variables):
            nombre = input("Nombre de la variable: ")
            valor = input(f"Valor de la variable '{nombre}': ")
            variables[nombre] = valor

        # Generar los resultados utilizando el generador de textos
        resultados = generador.generar(plantilla, variables)

        # Mostrar los resultados generados
        for nombre, texto in resultados.items():
            print(f"\nModelo: {nombre}\nTexto Generado:\n{texto}\n")

    # Mostrar la despedida después de la interacción completa
    presentacion.mostrarDespedida()

if __name__ == "__main__":
    # Llamar a la función que maneja la interfaz de usuario
    mostrar_interfaz()

    # Llamar a la función principal del generador de textos
    main()
