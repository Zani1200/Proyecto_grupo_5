import os
class Presentacion:

    def __init__(self):
        pass  # Constructor, puedes inicializar variables aquí si es necesario

    def printEncabezado(self):
        encabezado =  ("=======================================\n")
        encabezado += ("=== Bienvenido a Experiencias Viajeras ===\n")
        encabezado += ("=======================================\n")
        print(encabezado)
        return None

    def printMenu(self):
        menu = ("\n============ Menú ==============\n")
        menu += ("1. Lanza lo que quieras a Open IA\n")
        menu += ("2. Consultar base de datos\n")
        menu += ("3. Salir (o escribe 'salir')\n")
        print(menu)
        return None

    def limpiarConsola(self):
        os.system('cls')
        return None