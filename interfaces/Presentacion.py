import os

class Presentacion:
    def __init__(self):
        # Constructor, puedes inicializar variables aquí si es necesario
        pass

    # Menu bienvenida
    bienvenida = (
        "=========================================="
        "\n=== Bienvenido a Experiencias Viajeras ==="
        "\n=========================================="
    )

    menu = (
        "\n------------ Menú ------------------"
        "\n1. ¡Quiero una Experiencia Viajera!"
        "\n2. Consultar base de datos"
        "\n3. Salir (o escribe 'salir')"
        "\n------------------------------------\n"
    )

    planDeActividades = (
        "\nAquí tienes tu planificación para hoy, ¡esperamos que te guste!"
        "\nSi no es así, dinos qué quieres cambiar, por favor."
    )

    solicitarEntradaUsuario = (
        "\n¡Hola! Cuéntame, ¿qué te apetece hacer hoy? ¿Algo tranquilito para relajarte o más movidito para cargar pilas?"
        "\nSea lo que sea, ¡estoy aquí para ayudarte a encontrar el plan perfecto! ¿Cómo te sientes?"
    )

    solicitarMetadatos = (
        "\n¿Quieres añadir algo más? Te escuchamos. El formato es en parejas de característica-valor."
        "\nPor ejemplo: 'cielo': 'gris' o 'estado de ánimo': 'de bajón'."
        "\nSi no quieres añadir nada más, pulsa intro"
    )

    solicitarMasMetadatos = (
        "\n¿Algo más?. Recuerda que el formato es en parejas de característica-valor."
        "\nPor ejemplo: 'mi perro': 'está animado' o 'bolsillo': 'a tope de dólares'."
        "\nSi no quieres añadir nada más, pulsa intro"
    )

    despedida = (
        "\nGracias por contar conmigo ¡Pásalo muy bien hoy y luego me cuentas!"
        "\n¡Hasta pronto!"
    )

    def limpiarPantalla(self):
        """ Limpia la pantalla de la terminal (compatible con Windows y Unix). """
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrarBienvenida(self):
        self.limpiarPantalla()  # Limpiar la pantalla antes de mostrar la bienvenida
        print(self.bienvenida)

    def mostrarMenu(self):
        print(self.menu)

    def solicitarInputAlUsuario(self):
        print(self.solicitarEntradaUsuario)

    def solicitarMasDatosInicial(self):
        print(self.solicitarMetadatos)

    def solicitarMasDatosSucesivo(self):
        print(self.solicitarMasMetadatos)

    def mostrarDespedida(self):
        print(self.despedida)

    def mostrarPlanActividades(self, plan_actividades):
        print(self.planDeActividades)
        print(plan_actividades)
