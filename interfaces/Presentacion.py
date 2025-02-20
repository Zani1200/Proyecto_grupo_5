import os
import time
import json
from analisis.EnriquecerPeticionUsuario import procesar_peticion
from database.usuarios import Usuario


class Presentacion:
    def __init__(self, modelo_gpt, usuario: Usuario):
        """Inicializa la clase con un modelo GPT para generar respuestas."""
        self.modelo_gpt = modelo_gpt
        self.usuario = usuario


    def mostrar_menu(self):
        os.system("cls" if os.name == "nt" else "clear")  # Limpia la pantalla en Windows/Linux/Mac
        print("\n" + "=" * 50)
        print("🌍  🚀  BIENVENIDO A EXPERIENCIAS VIAJERAS  🚀  🌍")
        print("=" * 50 + "\n")

        print("📌 Selecciona una opción:")
        print("1️⃣  📍  Plan adaptado a ti")
        print("2️⃣  ✈️  Solicitar una experiencia viajera")
        print("3️⃣  📂  Ver base de datos")
        print("4️⃣  ❌  Salir\n")

        opcion = input("👉 Ingresa el número de la opción que deseas: ")
        return opcion

    def plan_adaptado(self, generador):
        """Genera un plan personalizado basado en la actividad y el nivel de energía del usuario."""
        print("\n🔹 Has seleccionado 'Plan adaptado a tu localización' 📍🌎")
        actividad_usuario = input("\n✍️ ¿Qué te gustaría hacer hoy? (Ejemplo: 'Quiero explorar museos') ")

        if actividad_usuario.lower() == "salir":
            return

        while True:
            try:
                nivel_energia = int(input("\n⚡ ¿Cuál es tu nivel de energía? (1: Bajo, 2: Medio, 3: Alto): "))
                energia = ""
                if nivel_energia in [1, 2, 3]:
                    if nivel_energia == 1:
                        energia = "bajo"
                    elif nivel_energia == 2:
                        energia = "medio"
                    else:
                        energia = "alto"
                    break
                else:
                    print("❌ Debes ingresar un número entre 1 y 3.")
            except ValueError:
                print("❌ Entrada no válida. Ingresa un número entre 1 y 3.")

        # Generar JSON con las respuestas del usuario
        datos_usuario = json.dumps({
            "actividad": actividad_usuario,
            "nivel_energia": energia
        }, indent=4)

        print("\n📜 Información recopilada en formato JSON:")
        print(datos_usuario)

        time.sleep(2)

        generador.generar(procesar_peticion(datos_usuario))


    def solicitar_experiencia(self):
        """Solicita una experiencia viajera y genera un texto basado en la petición del usuario."""
        print("\n🔹 Has seleccionado 'Solicitar una experiencia viajera' 🏝️✈️")

        peticion_usuario = input("\n✍️ ¿A donde vas? (Ejemplo: '¿Voy a Filipinas una semana?') ")

        if peticion_usuario.lower() == "salir":
            return

        # Enviar la petición al modelo GPT para extraer ciudad y actividad
        prompt_extraccion = (
            f"Analiza la siguiente petición y extrae la ciudad y la actividad: '{peticion_usuario}'.\n"
            "Devuelve el resultado en formato JSON con las claves 'ciudad' y 'actividad'."
        )

        respuesta = self.modelo_gpt.generar_texto(prompt_extraccion)

        # Procesar respuesta del modelo
        try:
            datos_extraidos = json.loads(respuesta)
            ciudad = datos_extraidos.get("ciudad", "desconocida")
            actividad = datos_extraidos.get("actividad", "desconocida")
        except json.JSONDecodeError:
            ciudad = "desconocida"
            actividad = "desconocida"

        print(f"\n📍 Ciudad detectada: {ciudad}")
        print(f"🎭 Actividad detectada: {actividad}")

        # Generar respuesta final con el modelo GPT
        prompt_final = f"Genera una experiencia viajera en {ciudad} para realizar {actividad}."
        resultado = self.modelo_gpt.generar_texto(prompt_final)

        print("\n📜 Experiencia recomendada:")
        print(resultado)

        time.sleep(2)

    def ver_base_datos(self):
        """Método de ejemplo para ver la base de datos."""
        print("\n🔹 Has seleccionado 'Ver base de datos' 📂📊")
        time.sleep(1)
        print("🚧 Función en construcción...")

    def mostrarDespedida(self):
        """Muestra mensaje de despedida."""
        print("\n👋 ¡Gracias por usar Experiencias Viajeras! Hasta la próxima. 🌍✨")
        time.sleep(2)
