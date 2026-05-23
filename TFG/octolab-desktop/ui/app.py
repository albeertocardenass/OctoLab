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
from config import APP_NAME

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.auth   = AuthManager()
        self.api    = ApiClient()
        self.docker = DockerManager()

        self.navbar  = None
        self.content = None

        self._mostrar_login()

    # -- NAVEGACIÓN ------------------------------------------------
    def _limpiar(self):
        for w in self.winfo_children():
            w.destroy()
        self.navbar  = None
        self.content = None

    def _mostrar_login(self):
        self._limpiar()
        LoginScreen(self, on_login=self._hacer_login).pack(fill="both", expand=True)

    def _hacer_login(self, email: str, password: str, on_error):
        def tarea():
            result = self.api.login(email, password)
            if result["ok"]:
                self.auth.guardar_sesion(result["data"])
                self.after(0, self._mostrar_dependencias)
            else:
                self.after(0, lambda: on_error(result["error"]))
        threading.Thread(target=tarea, daemon=True).start()

    def _mostrar_dependencias(self):
        self._limpiar()
        DependencyScreen(self, self.docker, on_ready=self._mostrar_home).pack(fill="both", expand=True)

    def _mostrar_home(self):
        self._limpiar()
        self._crear_layout()
        self._cargar_pantalla("inicio")

    def _crear_layout(self):
        self.navbar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.navbar.pack(side="left", fill="y")
        self.navbar.pack_propagate(False)

        ctk.CTkLabel(self.navbar, text="OctolabWeb",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#4f46e5").pack(pady=(30, 30))

        tabs = [
            ("🏠   Inicio",         "inicio"),
            ("💻  Laboratorios",    "labs"),
            ("📚  Temario",         "temario"),
            ("⚙️   Configuración",  "config"),
        ]
        for label, key in tabs:
            ctk.CTkButton(
                self.navbar, text=label, anchor="w",
                fg_color="transparent", hover_color="#1e293b",
                height=44, corner_radius=8,
                command=lambda k=key: self._cargar_pantalla(k)
            ).pack(fill="x", padx=12, pady=3)

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True)

    def _cargar_pantalla(self, key: str):
        for w in self.content.winfo_children():
            w.destroy()

        usuario = self.auth.usuario or {}

        pantallas = {
            "inicio":  lambda: HomeScreen(self.content, usuario),
            "labs":    lambda: LabsScreen(self.content, self.docker),
            "temario": lambda: TemarioScreen(self.content, usuario, self.api),
            "config":  lambda: ConfigScreen(self.content, usuario, self.auth,
                                             on_logout=self._mostrar_login),
        }
        pantallas[key]().pack(fill="both", expand=True)
