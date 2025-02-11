import os
class Presentacion:

    def __init__(self):
        pass  # Constructor, puedes inicializar variables aquí si es necesario

    # Menu bienvenida
    bienvenida = ("=========================================="
                  "\n=== Bienvenido a Experiencias Viajeras ==="
                  "\n==========================================")

    menu = ("\n------------ Menú ------------------"
            "\n"
            "\n1. ¡Quiero una Experiencias Viajera!"
            "\n2. Consultar base de datos"
            "\n3. Salir (o escribe 'salir')"
            "\n------------------------------------\n")

    planDeActividades = ("\nAquí tienes tu planificación para hoy, ¡esperamos que te guste!"
                         "\nSi no es así, dinos qué quieres cambiar, por favor.")

    solicitarEntradaUsuario = ("\n¡Hola! Cuéntame, ¿qué te apetece hacer hoy? ¿Algo tranquilito para relajarte o más movidito para cargar pilas? "
                               "\nSea lo que sea, ¡estoy aquí para ayudarte a encontrar el plan perfecto! ¿Cómo te sientes?")

    solicitarMetadatos = ("\n¿Quieres añadir algo más? Te escuchamos. El formato es en parejas de característica-valor. "
                          "\nPor ejemplo: 'cielo': 'gris' o 'estado de ánimo': 'de bajón'."
                          "\nSi no quieres añadir nada más, pulsa intro")

    solicitarMasMetadatos = ("\n¿Algo más?. Recuerda que el formato es en parejas de característica-valor."
                             "\nPor ejemplo: 'mi perro': 'está animado' o 'bolsillo': 'a tope de dólares'."
                             "\nSi no quieres añadir nada más, pulsa intro")

    despedida = ("\nGracias por contar conmigo ¡Pasalo muy bien hoy y luego me cuentas!"
                 "\n¡Hasta pronto!")

    planIA = ("\n Actividad 1"
              "\n Actividad 2"
              "\n etc."
              "\n etc.")

    def limpiarPantalla(self):
        os.system('cls')
        return None

    def mostrarBienvenida(self):
        print(self.bienvenida)
        return None

    def mostrarMenu(self):
        print(self.menu)
        return None

    def solicitarInputAlUsuario(self):
        print(self.solicitarEntradaUsuario)
        return None

    def solicitarMasDatosInicial(self):
        print(self.solicitarMetadatos)
        return None

    def solicitarMasDatosSucesivo(self):
        print(self.solicitarMasMetadatos)
        return None

    def mostrarDespedida(self):
        print(self.despedida)
        return None

    def mostrarPlanActividades(self,planIA):
        print(self.planDeActividades)
        return None

