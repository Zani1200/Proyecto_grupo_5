import sqlite3


class BaseDeDatos:

    def __init__(self):
        self.conn = sqlite3.connect("ProyectoExperienciasViajeras")
        self.cursor = self.conn.cursor()
        self.crearTablas()
        self.cursor.execute("DELETE FROM prompt")
        self.cursor.execute("DELETE FROM respuestas")

    def crearTablas(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt (
            id INTEGER PRIMARY KEY,
            texto TEXT NOT NULL);
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS respuestas (
            id INTEGER PRIMARY KEY,
            prompt_id INTEGER NOT NULL,
            texto TEXT NOT NULL,
            FOREIGN KEY (prompt_id) REFERENCES prompt (id) ON DELETE CASCADE ON UPDATE CASCADE);
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS variables_entorno (
            id INTEGER PRIMARY KEY,
            prompt_id INTEGER NOT NULL,
            atributo TEXT NOT NULL,
            valor TEXT NOT NULL,
            FOREIGN KEY (prompt_id) REFERENCES prompt (id) ON DELETE CASCADE ON UPDATE CASCADE);
        """)

        self.conn.commit()

    def guardarPrompt(self, prompt):
        self.cursor.execute("""
        INSERT INTO prompt (texto)
        VALUES(?)
        """, (prompt,))
        self.conn.commit()
        return self.cursor.lastrowid  # Sirve para sacar el id de este INSERT

    def guardarRespuesta(self, prompt_id, respuesta):
        self.cursor.execute("""
        INSERT INTO respuestas (prompt_id, texto)
        VALUES(?,?)
        """, (prompt_id, respuesta,))
        self.conn.commit()

    def guardarVariablesEntorno(self, prompt_id, atributo, valor):
        self.cursor.execute("""
        INSERT INTO variables_entorno (prompt_id, atributo, valor)
        VALUES(?,?,?)
        """, (prompt_id, atributo, valor,))
        self.conn.commit()

    def verDatos(self):
        self.cursor.execute("""SELECT prompt.id, prompt.texto, respuestas.texto, variables_entorno.atributo, variables_entorno.valor 
        FROM prompt 
        INNER JOIN respuestas 
        ON prompt.id = respuestas.prompt_id 
        INNER JOIN variables_entorno 
        ON prompt.id = variables_entorno.prompt_id
        """)

        columnas = self.cursor.fetchall()

        for columna in columnas:
            print(columna)


if __name__ == "__main__":
    crear = BaseDeDatos()
    while True:
        prompt = input(str("pon un texto\n"))
        prompt_id = crear.guardarPrompt(prompt)
        print(prompt_id)
        while True:
            plantilla = input("Ingresa las variables que necesites (o 'salir' para terminar): ")
            if plantilla.lower() == 'salir':
                break
            atributo = input("dime el nombre de la variables\n")
            valor = input(f"dime el valor de {atributo}\n")
            crear.guardarVariablesEntorno(prompt_id, atributo, valor)
        crear.guardarRespuesta(prompt_id, "Hola Pedro3")
        crear.verDatos()
