class SingletonMeta(type):
    """Metaclase que implementa el patrón Singleton.

    Este patrón asegura que una clase tenga solo una instancia.
    Si se intenta crear una nueva instancia, la metaclase devolverá la instancia existente.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Crea la instancia solo si no existe, si ya existe la devuelve.

        :param args: Argumentos posicionales para la clase.
        :param kwargs: Argumentos keyword para la clase.
        :return: Instancia única de la clase.
        """
        if cls not in cls._instances:
            # Si la instancia aún no existe, la crea.
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
            print(f"Instancia de {cls.__name__} creada.")
        else:
            print(f"Instancia de {cls.__name__} ya existe, devolviendo la instancia existente.")

        return cls._instances[cls]
