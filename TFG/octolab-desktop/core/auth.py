import json
import os
from config import SESSION_FILE

class AuthManager:
    def __init__(self):
        self.usuario = None

    def guardar_sesion(self, usuario: dict):
        self.usuario = usuario
        with open(SESSION_FILE, "w") as f:
            json.dump(usuario, f)

    def cargar_sesion(self) -> dict | None:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE) as f:
                self.usuario = json.load(f)
                return self.usuario
        return None

    def cerrar_sesion(self):
        self.usuario = None
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    def esta_logueado(self) -> bool:
        return self.usuario is not None
