import sys
from pathlib import Path

from database.base_datos_Supabase import BaseDatos

# Ajustar el sys.path para incluir la ruta al directorio raíz del proyecto
# Esto permite que Python encuentre el módulo 'database' incluso si ejecutas desde 'fastAPI'
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict


app = FastAPI()

# Crear instancia de BaseDatos
def get_database():
    return BaseDatos()

class UsuarioAPI(BaseModel):
    id: int = Field(default=None, allow_mutation=False)
    apodo: str = Field(..., min_length=2)
    correo: EmailStr
    contraseña: str

# Modelo para actualizar datos (el apodo no se puede cambiar)
class UsuarioUpdate(BaseModel):
    correo: Optional[EmailStr] = None
    contraseña: Optional[str] = None


class PreguntaRespuesta(BaseModel):
    id_usuario: int
    pregunta: str
    respuesta: str
    variables: Dict

@app.get("/")
def bienvenidos():
    return {"Bienvenidos": "Backend de gestion de datos de usuarios de Experiencias Viajeras"}

# CREAR Usuario
@app.post("/usuarios/crear/", response_model=dict)
def create_usuario(usuarioAPI: UsuarioAPI, db: BaseDatos = Depends(get_database)):
    success = db.crear_usuario(usuarioAPI.apodo, usuarioAPI.correo, usuarioAPI.contraseña)
    if not success:
        raise HTTPException(status_code=400, detail="Error al crear el usuario")

    return {"message": "Usuario creado correctamente"}

# OBTENER Usuario por ID
@app.get("/usuarios/{id}", response_model=UsuarioAPI)
def read_usuario(id: int, db: BaseDatos = Depends(get_database)):
    response = db.consultar_usuario(id)

    if response:
        usuarioDB = response[0]
        idDB = usuarioDB.get("id")
        apodoDB = usuarioDB.get("apodo")
        correoDB = usuarioDB.get("correo")
        contraseñaDB = usuarioDB.get("contraseña")

        usuarioAPI = UsuarioAPI(id=idDB, apodo=apodoDB, correo=correoDB, contraseña=contraseñaDB)
    else:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")

    return usuarioAPI

# ACTUALIZAR Usuario
@app.put("/usuarios/{id}", response_model=dict)
def update_usuario(id: int, usuario: UsuarioUpdate, db: BaseDatos = Depends(get_database)):
    response = db.consultar_usuario(id)
    print("DB response", response)

    print("Usuario", usuario)
    if not response:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    response = db.modificar_usuario(id, usuario.correo, usuario.contraseña)

    if not response:
        raise HTTPException(status_code=400, detail=f"Error al actualizar el usuario con id {id}")

    return {"message": "Usuario actualizado correctamente"}

# ELIMINAR Usuario
@app.delete("/usuarios/{id}", response_model=dict)
def delete_usuario(id: int, db: BaseDatos = Depends(get_database)):
    response = db.borrar_usuario(id)

    if not response.data:
        raise HTTPException(status_code=400, detail=f"Error al eliminar el usuario {id}, verifique que exista")

    return {"message": "Usuario eliminado correctamente"}

# LISTAR Usuarios
@app.get("/usuarios/listar/", response_model=List[UsuarioAPI])
def list_usuarios(db: BaseDatos = Depends(get_database)):
    usuarios = db.listar_usuarios()
    return usuarios


@app.get("/usuarios/verificar/", response_model=dict)
def verificar_usuario(apodo: str, correo: EmailStr, contraseña: str, db: BaseDatos = Depends(get_database)):
    verificacion = db.verificar_usuario(apodo, correo, contraseña)
    if not db.verificar_usuario(apodo, correo, contraseña):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"id": verificacion["id"]}


@app.post(path="/pregunta_respuesta/insertar", response_model=dict)
def insertar_pregunta_respuesta(pregunta_respuesta: PreguntaRespuesta, db: BaseDatos = Depends(get_database)):
    # Desestructuramos los datos del modelo
    id_usuario = pregunta_respuesta.id_usuario
    respuesta = pregunta_respuesta.respuesta
    pregunta = pregunta_respuesta.pregunta
    variables = pregunta_respuesta.variables
    success = db.insertar_pregunta_respuesta(variables, respuesta, pregunta, id_usuario)
    if not success:
        raise HTTPException(status_code=401, detail="Error al insertar")

    return {"message": "Insertado correctamente"}