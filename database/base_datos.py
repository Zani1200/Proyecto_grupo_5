import sqlite3
from ..utils import singleton

class BaseDeDatos(metaclass=singleton.SingletonMeta):

    def __init__(self):
        self.conn = sqlite3.connect("ProyectoExperienciasViajeras.db")
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt (
                id INTEGER PRIMARY KEY,
                texto TEXT NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS respuestas (
                id INTEGER PRIMARY KEY,
                prompt_id INTEGER NOT NULL,
                texto TEXT NOT NULL,
                FOREIGN KEY (prompt_id) REFERENCES prompt (id) ON DELETE CASCADE
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS variables_entorno (
                id INTEGER PRIMARY KEY,
                prompt_id INTEGER NOT NULL,
                atributo TEXT NOT NULL,
                valor TEXT NOT NULL,
                FOREIGN KEY (prompt_id) REFERENCES prompt (id) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    def limpiarBaseDatos(self):
        """ Elimina todos los datos de la base de datos. """
        try:
            confirmacion = input("¿Estás seguro de que quieres limpiar la base de datos? (Sí/No): ")
            if confirmacion.lower() == 'sí':
                self.cursor.execute("DELETE FROM prompt")
                self.cursor.execute("DELETE FROM respuestas")
                self.cursor.execute("DELETE FROM variables_entorno")
                self.conn.commit()
                print("📌 Base de datos limpiada correctamente.")
            else:
                print("❌ Operación cancelada.")
        except Exception as e:
            print("❌ Error al limpiar la base de datos:", e)

    def guardarPrompt(self, prompt):
        """ Guarda un nuevo prompt en la base de datos. """
        try:
            self.cursor.execute("INSERT INTO prompt (texto) VALUES (?)", (prompt,))
            self.conn.commit()
            return self.cursor.lastrowid  # Retorna el ID del prompt insertado
        except Exception as e:
            print("❌ Error al guardar el prompt:", e)

    def guardarRespuesta(self, prompt_id, respuesta):
        """ Guarda una respuesta asociada a un prompt. """
        try:
            self.cursor.execute("INSERT INTO respuestas (prompt_id, texto) VALUES (?, ?)", (prompt_id, respuesta))
            self.conn.commit()
        except Exception as e:
            print("❌ Error al guardar la respuesta:", e)

    def guardarVariablesEntorno(self, prompt_id, atributo, valor):
        """ Guarda variables de entorno asociadas a un prompt. """
        try:
            self.cursor.execute("INSERT INTO variables_entorno (prompt_id, atributo, valor) VALUES (?, ?, ?)",
                                (prompt_id, atributo, valor))
            self.conn.commit()
        except Exception as e:
            print("❌ Error al guardar la variable de entorno:", e)

    def verDatos(self):
        """ Muestra los datos almacenados en la base de datos. """
        try:
            self.cursor.execute("""
                SELECT prompt.id, prompt.texto, respuestas.texto, variables_entorno.atributo, variables_entorno.valor 
                FROM prompt 
                LEFT JOIN respuestas ON prompt.id = respuestas.prompt_id 
                LEFT JOIN variables_entorno ON prompt.id = variables_entorno.prompt_id
            """)

            columnas = self.cursor.fetchall()
            for columna in columnas:
                print(columna)
        except Exception as e:
            print("❌ Error al obtener los datos:", e)

    def __del__(self):
        """ Cierra la conexión con la base de datos al eliminar la instancia. """
        self.conn.close()
        print("📌 Conexión a la base de datos cerrada.")

# 🌟 PRUEBA INTERACTIVA
if __name__ == "__main__":
    bd = BaseDeDatos()

    while True:
        prompt = input("\n📌 Ingresa un nuevo prompt (o 'salir' para terminar): ")
        if prompt.lower() == "salir":
            break

        prompt_id = bd.guardarPrompt(prompt)
        print(f"✅ Prompt guardado con ID {prompt_id}")

        while True:
            var_nombre = input("🔹 Nombre de la variable (o 'salir' para terminar): ")
            if var_nombre.lower() == "salir":
                break
            var_valor = input(f"💡 Valor para '{var_nombre}': ")
            bd.guardarVariablesEntorno(prompt_id, var_nombre, var_valor)

        respuesta = input("💬 Ingresa una respuesta para este prompt: ")
        bd.guardarRespuesta(prompt_id, respuesta)

        bd.verDatos()
