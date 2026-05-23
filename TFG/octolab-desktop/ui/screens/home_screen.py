import customtkinter as ctk

class HomeScreen(ctk.CTkFrame):
    def __init__(self, master, usuario: dict):
        super().__init__(master, fg_color="transparent")
        self.usuario = usuario
        self._build()

    def _build(self):
        nombre = self.usuario.get("nombre", "Usuario")
        rol    = self.usuario.get("rol", "Usuario")
        puntos = self.usuario.get("puntos", 0)

        ctk.CTkLabel(self, text=f"Bienvenido, {nombre} 👋",
                     font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(40, 6))
        ctk.CTkLabel(self, text=f"Rol: {rol}  •  Puntos: {puntos}",
                     text_color="gray", font=ctk.CTkFont(size=13)).pack(pady=(0, 40))

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack()

        cards = [
            ("💻", "Laboratorios",   "Accede a Kali y Metasploitable"),
            ("📚", "Temario",        "Tests y contenido formativo"),
            ("⚙️", "Configuración",  "Ajustes de la app"),
        ]
        for icon, titulo, desc in cards:
            card = ctk.CTkFrame(grid, corner_radius=12, width=180, height=140)
            card.grid_propagate(False)
            card.pack(side="left", padx=16, pady=10)
            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=32)).pack(pady=(20, 4))
            ctk.CTkLabel(card, text=titulo,
                         font=ctk.CTkFont(size=14, weight="bold")).pack()
            ctk.CTkLabel(card, text=desc, text_color="gray",
                         font=ctk.CTkFont(size=11), wraplength=150).pack(pady=4)
