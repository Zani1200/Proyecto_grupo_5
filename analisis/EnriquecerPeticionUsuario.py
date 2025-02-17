import json
from datetime import datetime
from openai import OpenAI


# Simulación de funciones para obtener información adicional
def obtener_hora_local():
    return datetime.now().isoformat()

def obtener_ubicacion():
    return {"ciudad": "Oranjestad", "pais": "Aruba"}

def obtener_clima():
    return {"temperatura": "15°C", "condición": "Soleado"}

def obtener_nivel_energia():
    return "Medio"

def obtener_estado_animo():
    return "Motivado"

def obtener_estado_emocional(texto):
    """Consulta a OpenAI para analizar el estado emocional basado en la petición del usuario."""

    client = OpenAI()

    respuesta = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user",
                   "content": f"Analiza el siguiente mensaje y dime en una palabra su estado emocional: {texto}"}]
    )
    return respuesta.choices[0].message.content.strip()


def procesar_peticion(peticion_json):
    peticion = json.loads(peticion_json)

    peticion_usuario = peticion.get("peticion_usuario", "")
    nivel_energia = peticion.get("nivel_energia", "2")

    estado_emocional = obtener_estado_emocional(peticion_usuario)

    respuesta = {
        "peticion_usuario": peticion_usuario,
        "nivel_energia": nivel_energia,
        "estado_emocional": estado_emocional,
        "localizacion": obtener_ubicacion(),
        "tiempo": obtener_clima(),
        "hora_local": obtener_hora_local()
    }

    return json.dumps(respuesta, indent=4, ensure_ascii=False)


# Ejemplo de uso
entrada_json = json.dumps({
    "peticion_usuario": "Me apetecería darme un buen baño en algún sitio molón.",
    "nivel_energia": "3"
})

salida_json = procesar_peticion(entrada_json)
print(salida_json)