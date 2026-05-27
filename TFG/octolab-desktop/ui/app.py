import customtkinter as ctk
import threading
from core.auth import AuthManager
from core.api_client import ApiClient
from core.docker_manager import DockerManager
from ui.screens.login_screen import LoginScreen
from ui.screens.dependency_screen import DependencyScreen
from ui.screens.home_screen import HomeScreen
from ui.screens.labs_screen import LabsScreen
from ui.screens.temario_screen import TemarioScreen
from ui.screens.config_screen import ConfigScreen
from config import APP_NAME, THEME_FILE, IMAGES_DIR

import os, json

class App(ctk.CTk):
    def __init__(self):
        # Cargar tema guardado antes de inicializar la ventana
        tema = self._cargar_tema()
        ctk.set_appearance_mode(tema)
        ctk.set_default_color_theme("blue")

        super().__init__()
        self.title(APP_NAME)
        self.geometry("1100x700")                      # tamaño inicial mientras carga
        self.after(10, lambda: self.state("zoomed"))   # maximizar tras el primer frame

        # Icono de la ventana
        _ico = os.path.join(IMAGES_DIR, "octolab.ico")
        if os.path.exists(_ico):
            self.iconbitmap(_ico)

        self.auth   = AuthManager()
        self.api    = ApiClient()
        self.docker = DockerManager()

        self.navbar  = None
        self.content = None

        self._mostrar_login()

    def _cargar_tema(self) -> str:
        try:
            if os.path.exists(THEME_FILE):
                with open(THEME_FILE) as f:
                    return json.load(f).get("tema", "Dark")
        except Exception:
            pass
        return "Dark"

    # -- NAVEGACIÓN ------------------------------------------------
    def _limpiar(self):
        for w in self.winfo_children():
            w.destroy()
        self.navbar  = None
        self.content = None

    def _mostrar_login(self):
        self._limpiar()
        LoginScreen(self,
                    on_login=self._hacer_login,
                    on_guest=self._hacer_login_invitado).pack(fill="both", expand=True)

    def _hacer_login(self, email: str, password: str, on_error):
        def tarea():
            result = self.api.login(email, password)
            if result["ok"]:
                self.auth.guardar_sesion(result["data"])
                self.after(0, self._mostrar_dependencias)
            else:
                self.after(0, lambda: on_error(result["error"]))
        threading.Thread(target=tarea, daemon=True).start()

    def _hacer_login_invitado(self):
        invitado = {
            "id": 0,
            "nombre": "Invitado",
            "apodo": "Invitado",
            "email": "",
            "rol": "Invitado",
            "avatar": None,
            "modulosDesbloqueados": [],
        }
        self.auth.guardar_sesion(invitado)
        self._mostrar_dependencias()

    def _mostrar_dependencias(self):
        self._limpiar()
        DependencyScreen(self, self.docker, on_ready=self._mostrar_home).pack(fill="both", expand=True)

    def _mostrar_home(self):
        self._limpiar()
        self._crear_layout()
        self._cargar_pantalla("inicio")

    def _crear_layout(self):
        self.navbar = ctk.CTkFrame(self, width=200, corner_radius=0,
                                   fg_color=("gray88", "#0f172a"),
                                   border_width=0)
        self.navbar.pack(side="left", fill="y")
        self.navbar.pack_propagate(False)

        ctk.CTkLabel(
            self.navbar, text="OctoLab",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#4f46e5"
        ).pack(pady=(22, 22))

        tabs = [
            ("Inicio",         "inicio"),
            ("Laboratorios",   "labs"),
            ("Temario",        "temario"),
            ("Configuracion",  "config"),
        ]
        self._nav_buttons = {}
        for label, key in tabs:
            btn = ctk.CTkButton(
                self.navbar, text=label, anchor="w",
                fg_color="transparent",
                hover_color=("gray75", "#1e293b"),
                text_color=("gray15", "gray90"),
                height=48, corner_radius=8,
                font=ctk.CTkFont(size=16),
                command=lambda k=key: self._cargar_pantalla(k)
            )
            btn.pack(fill="x", padx=12, pady=3)
            self._nav_buttons[key] = btn

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True)

    def _cargar_pantalla(self, key: str):
        for w in self.content.winfo_children():
            w.destroy()

        # Resaltar pestaña activa
        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.configure(fg_color=("gray75", "#1e293b"),
                               text_color=("#4f46e5", "#818cf8"),
                               font=ctk.CTkFont(size=16, weight="bold"))
            else:
                btn.configure(fg_color="transparent",
                               text_color=("gray15", "gray90"),
                               font=ctk.CTkFont(size=16))

        usuario = self.auth.usuario or {}

        pantallas = {
            "inicio":  lambda: HomeScreen(self.content, usuario, self.api),
            "labs":    lambda: LabsScreen(self.content, self.docker),
            "temario": lambda: TemarioScreen(self.content, usuario, self.api),
            "config":  lambda: ConfigScreen(self.content, usuario, self.auth,
                                             on_logout=self._mostrar_login),
        }
        pantallas[key]().pack(fill="both", expand=True)
