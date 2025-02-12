import os
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

    def generar(self, plantilla, variables):
        """ Generar texto basado en una plantilla y variables. """
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
    api_key = os.getenv("OPENAI_API_KEY")  # Obtener la clave de API desde variables de entorno

    if not api_key:
        print("❌ ERROR: La API key de OpenAI no está configurada.")
        return

    modelo_gpt = ModeloGPT("GPT-4", "v1.0", api_key)
    generador.agregar_modelo(modelo_gpt)

    while True:
        print("\n=== Generador de Textos Personalizado ===")
        plantilla = input("📝 Ingresa una plantilla de prompt (o 'salir' para terminar): ").strip()

        if plantilla.lower() == 'salir':
            print("👋 Saliendo del programa...")
            break

        # Validar entrada numérica
        while True:
            num_variables_str = input("🔢 ¿Cuántas variables deseas ingresar? ")
            if num_variables_str.isdigit():  # Verifica si es un número válido
                num_variables = int(num_variables_str)
                if num_variables > 0:
                    break
                else:
                    print("⚠️ Debes ingresar al menos una variable.")
            else:
                print("❌ Error: Ingresa un número válido.")

        # Capturar variables
        variables = {}
        for _ in range(num_variables):
            clave = input("🔑 Nombre de la variable: ").strip()
            valor = input(f"📌 Valor para '{clave}': ").strip()
            variables[clave] = valor

        # Generar textos con la IA
        try:
            print("⚙️ Generando texto con los datos proporcionados...")
            resultados = generador.generar(plantilla, variables)

            if resultados:
                for nombre, texto in resultados.items():
                    print(f"\n📜 Modelo: {nombre}\n📝 Texto Generado:\n{texto}\n")
            else:
                print("⚠️ No se generaron resultados.")

        except Exception as e:
            print(f"❌ Error inesperado al generar texto: {e}")

if __name__ == "__main__":
    mostrar_interfaz()
    main()
