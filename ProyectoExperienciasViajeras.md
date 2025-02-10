PROPÓSITO DEL PROGRAMA: Sugerir experiencias de ocio para el día

DESCRIPCIÓN: 

El programa tiene que ofrecer una planificación de actividades para el día en función de lo 
que el usuario pida, y de su nivel de energía, estado de ánimo, presupuesto, localización, la meteorología, 
la hora en ese momento, etc. El programa detectará a partir del input del usuario el nivel de energía de 
éste, y creará la planificiación en base a ello.

El usuario puede añadir tantos parámetros como desee (qué le apetece hacer, presupuesto, si quiere algo 
tranquilo o más animado, etc.). Lo puede hacer mediante audio, haciéndose una foto, y por texto.

Cuando el usuario recibe la propuesta, puede valorarla, sugerir cambios, y pedir una nueva. Esto lo puede
hacer cuantas veces quiera.

MEJORA (si da tiempo): se guardan en basa de datos las propuestas, y si un nuevo usuario se encuentra 
en una situación similar al de alguna propuesta anterior (localización, estado de ánimo, meteorología),
se le muestra.

-------------------

IMPLEMENTACIÓN EN MÓDULOS

Se divide el programa en varios módulos:
 
1. Interacción con el usuario
2. Análisis de la situación del usuario: decidir el estado de ánimo, meteorología, hora, inputs, etc.
3. Propuesta del plan de ocio: interacción con la IA
4. Presentación del plan y corrección por parte del usuario
5. Manejo de base de datos para presentar al usuario (opcional, para la mejora)

-------------------

DISEÑO

Clases:

- Presentacion
- Base de datos
- Principal
- Interacciones con otras APIs (IA, weather)
- Prompts y plantillas

-------------------

FLUJO

1. Bienvenida a la app (¿usar chatGPT?)
2. Interacción con el usuario para recibir su input acerca de qué necesita (¿usar chatGPT?). 2.1 Iterar hasta que el usuario haya terminado
   - Iterar hasta que el usuario quiera
   - Ofrecer distintos tipos de input (video, audio, texto)
   - Para cada uno de ellos, ofrecer el nombre del atributo, por ejemplo: localización, 
      estado de ánimo, nivel de energía, etc.
3. Analizar el input para inferir el nivel de energía y el estado de ánimo del usuario
4. Obtener datos adicionales: ubicación, hora local y tiempo (usar weather API)
5. Obtener plan de la IA
6. Mostrar propuesta al usuario
7. Pedir feedback al usuario
8. Iterar 5 y 6 hasta que el usuario de el OK.
9. Guardar en base de datos
10. Despedida. Mensaje y cerrar base de datos.

