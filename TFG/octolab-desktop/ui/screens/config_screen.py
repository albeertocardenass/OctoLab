import customtkinter as ctk
from config import APP_VERSION

class ConfigScreen(ctk.CTkFrame):
    def __init__(self, master, usuario: dict, auth_manager, on_logout):
        super().__init__(master, fg_color="transparent")
        self.usuario      = usuario
        self.auth_manager = auth_manager
        self.on_logout    = on_logout
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Configuración",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 20))

        card = ctk.CTkFrame(self, corner_radius=12, width=420)
        card.pack(padx=40)
        card.pack_propagate(False)

        nombre = self.usuario.get("nombre", "")
        email  = self.usuario.get("email", "")
        rol    = self.usuario.get("rol", "")

        ctk.CTkLabel(card, text=f"👤  {nombre}",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=24, pady=(24, 2))
        ctk.CTkLabel(card, text=f"✉️  {email}",
                     text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=24)
        ctk.CTkLabel(card, text=f"🎭  {rol}",
                     text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=24, pady=(2, 20))

        ctk.CTkFrame(card, height=1, fg_color="#334155").pack(fill="x", padx=20)

        theme_frame = ctk.CTkFrame(card, fg_color="transparent")
        theme_frame.pack(fill="x", padx=24, pady=16)
        ctk.CTkLabel(theme_frame, text="Tema oscuro",
                     font=ctk.CTkFont(size=13)).pack(side="left")
        self.theme_switch = ctk.CTkSwitch(theme_frame, text="",
                                           command=self._toggle_theme)
        self.theme_switch.pack(side="right")
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

        ctk.CTkFrame(card, height=1, fg_color="#334155").pack(fill="x", padx=20)

        ctk.CTkLabel(card, text=f"Versión {APP_VERSION}",
                     text_color="gray", font=ctk.CTkFont(size=11)).pack(pady=12)

        ctk.CTkButton(card, text="Cerrar Sesión", width=360, height=42,
                       fg_color="#ef4444", hover_color="#dc2626",
                       command=self._logout).pack(pady=(0, 24))

    def _toggle_theme(self):
        modo = "Dark" if self.theme_switch.get() else "Light"
        ctk.set_appearance_mode(modo)

    def _logout(self):
        self.auth_manager.cerrar_sesion()
        self.on_logout()
