import customtkinter as ctk

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master, fg_color="transparent")
        self.on_login = on_login
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Octolab", font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="#4f46e5").pack(pady=(60, 0))
        ctk.CTkLabel(self, text="Plataforma de Ciberseguridad",
                     font=ctk.CTkFont(size=14), text_color="gray").pack(pady=(4, 40))

        card = ctk.CTkFrame(self, corner_radius=16, width=380)
        card.pack(padx=40, pady=10)
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="Iniciar Sesión",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(30, 20))

        self.email_var = ctk.StringVar()
        self.pass_var  = ctk.StringVar()
        self.error_var = ctk.StringVar()

        ctk.CTkEntry(card, placeholder_text="Correo electrónico",
                     textvariable=self.email_var, width=300, height=42).pack(pady=6)

        ctk.CTkEntry(card, placeholder_text="Contraseña",
                     textvariable=self.pass_var, show="*",
                     width=300, height=42).pack(pady=6)

        ctk.CTkLabel(card, textvariable=self.error_var,
                     text_color="#ef4444", font=ctk.CTkFont(size=12)).pack(pady=4)

        self.btn = ctk.CTkButton(card, text="Entrar", width=300, height=42,
                                  fg_color="#4f46e5", hover_color="#4338ca",
                                  command=self._login)
        self.btn.pack(pady=(6, 30))

    def _login(self):
        self.error_var.set("")
        self.btn.configure(state="disabled", text="Conectando...")
        email    = self.email_var.get().strip()
        password = self.pass_var.get()

        if not email or not password:
            self.error_var.set("Completa todos los campos.")
            self.btn.configure(state="normal", text="Entrar")
            return

        self.on_login(email, password, self._on_error)

    def _on_error(self, msg: str):
        self.error_var.set(msg)
        self.btn.configure(state="normal", text="Entrar")
