class Usuario:

    def __init__(self, apodo, correo, contraseña):
        self._apodo = apodo
        self._correo = correo
        self._contraseña = contraseña

    @property
    def apodo(self):
        return self._apodo

    @apodo.setter
    def apodo(self, nuevo_apodo):
        self._apodo = nuevo_apodo
    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, nuevo_correo):
        self._correo = nuevo_correo
    @property
    def contraseña(self):
        return self._contraseña

    @contraseña.setter
    def contraseña(self, nueva_contraseña):
        self._contraseña = nueva_contraseña