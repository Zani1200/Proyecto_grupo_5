from Proyecto_Grupo_5 import ModeloGenerativo
from Proyecto_Grupo_5.ModeloGPT import ModeloGPT
from Proyecto_Grupo_5.Presentacion import Presentacion


class GeneradorTextos:
    def __init__(self):
        self.modelos = []

    def agregar_modelo(self, modelo):
        #if isinstance(modelo, ModeloGenerativo):
        if isinstance(modelo, ModeloGPT):
            self.modelos.append(modelo)
        else:
            raise TypeError("El modelo debe ser una instancia de ModeloGenerativo.")

    def generar(self, plantilla, variables):
        textos = {}
        for modelo in self.modelos:
            texto = modelo.obtener_respuesta(plantilla, variables)
            textos[modelo.nombre] = texto
        return textos

def main():

    presentacion = Presentacion()
    presentacion.mostrarBienvenida()
    print("\n")
    print("*" * 50)
    presentacion.mostrarMenu()
    print("\n")
    print("*" * 50)
    presentacion.solicitarInputAlUsuario()
    print("\n")
    print("*" * 50)
    presentacion.solicitarMasDatosInicial()
    print("\n")
    print("*" * 50)
    presentacion.solicitarMasDatosSucesivo()
    print("\n")
    print("*" * 50)
    presentacion.mostrarPlanActividades(presentacion.planIA)
    print("\n")
    print("*" * 50)
    presentacion.mostrarDespedida()
    print("\n")
    print("*" * 50)

    """
    # Crear instancias de modelos
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", "tu_api_key")
    # Puedes agregar más modelos si los tienes
    # modelo_otro = OtroModelo("OtroModel", "v2.0", "otro_api_key")

    # Crear el generador de textos y agregar los modelos
    generador = GeneradorTextos()
    generador.agregar_modelo(modelo_gpt)
    # generador.agregar_modelo(modelo_otro)

    # Interacción con el usuario
    while True:
        print("=== Generador de Textos Personalizado ===")
        plantilla = input("Ingresa una plantilla de prompt (o 'salir' para terminar): ")
        if plantilla.lower() == 'salir':
            break
        num_variables = int(input("¿Cuántas variables deseas ingresar? "))
        variables = {}
        for _ in range(num_variables):
            clave = input("Nombre de la variable: ")
            valor = input(f"Valor para '{clave}': ")
            variables[clave] = valor

        # Generar textos
        resultados = generador.generar(plantilla, variables)

        # Mostrar resultados
        for nombre, texto in resultados.items():
            print(f"\nModelo: {nombre}\nTexto Generado:\n{texto}\n")
"""

if __name__ == "__main__":
    main()