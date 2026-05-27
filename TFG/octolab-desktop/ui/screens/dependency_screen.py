"""
dependency_screen.py — Comprobación rápida del entorno tras el login.
Verifica si Docker está disponible y ofrece activarlo si no lo está.
"""
import threading
import customtkinter as ctk

C = {
    "primary":  "#4f46e5",
    "card":     ("gray92", "#1e293b"),
    "muted":    ("gray40", "#94a3b8"),
    "ok":       "#10b981",
    "warn":     "#f59e0b",
    "divider":  ("gray80", "#334155"),
}


class DependencyScreen(ctk.CTkFrame):
    def __init__(self, master, docker_manager, on_ready):
        super().__init__(master, fg_color="transparent")
        self.docker_manager = docker_manager
        self.on_ready       = on_ready
        self._activando     = False
        self._build()
        threading.Thread(target=self._verificar, daemon=True).start()

    # ── UI ────────────────────────────────────────────────────────────
    def _build(self):
        ctk.CTkFrame(self, fg_color="transparent").pack(expand=True)

        self._panel = ctk.CTkFrame(self, fg_color="transparent")
        self._panel.pack()

        ctk.CTkLabel(self._panel,
                     text="Verificando entorno",
                     font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(0, 6))
        ctk.CTkLabel(self._panel,
                     text="Comprobando los requisitos necesarios para la aplicación...",
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=15)).pack(pady=(0, 24))

        # ── Tarjeta de estado ─────────────────────────────────────────
        card = ctk.CTkFrame(self._panel, corner_radius=14,
                            fg_color=C["card"], width=440)
        card.pack(pady=(0, 24))
        card.pack_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=24, pady=20)

        # Fila principal
        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x")

        ico = ctk.CTkFrame(row, width=38, height=38,
                           corner_radius=8, fg_color=("gray82", "#334155"))
        ico.pack(side="left")
        ico.pack_propagate(False)
        ctk.CTkLabel(ico, text="D",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=C["primary"]).place(relx=0.5, rely=0.5, anchor="center")

        desc = ctk.CTkFrame(row, fg_color="transparent")
        desc.pack(side="left", padx=(12, 0), fill="x", expand=True)
        ctk.CTkLabel(desc, text="Docker Desktop",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     anchor="w").pack(anchor="w")
        ctk.CTkLabel(desc, text="Necesario para los Laboratorios",
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=13),
                     anchor="w").pack(anchor="w")

        # Badge de estado
        self._badge = ctk.CTkFrame(row, corner_radius=8,
                                   fg_color=("gray80", "#334155"))
        self._badge.pack(side="right")
        self._badge_lbl = ctk.CTkLabel(self._badge, text="Comprobando...",
                                        text_color=C["muted"],
                                        font=ctk.CTkFont(size=11, weight="bold"))
        self._badge_lbl.pack(padx=10, pady=5)

        # Mensaje de aviso (oculto hasta que se necesite)
        self._warn_lbl = ctk.CTkLabel(inner, text="",
                                       text_color=C["warn"],
                                       font=ctk.CTkFont(size=12),
                                       wraplength=380, justify="left")
        self._warn_lbl.pack(anchor="w", pady=(12, 0))

        # ── Spinner ───────────────────────────────────────────────────
        self._bar = ctk.CTkProgressBar(self._panel, width=400, height=4,
                                        mode="indeterminate",
                                        progress_color=C["primary"])
        self._bar.pack(pady=(0, 28))
        self._bar.start()

        # ── Fila de botones (oculta hasta finalizar comprobación) ─────
        self._btn_row = ctk.CTkFrame(self._panel, fg_color="transparent")

        self._btn_activar = ctk.CTkButton(
            self._btn_row,
            text="Activar Docker",
            width=210, height=46,
            fg_color=C["ok"], hover_color="#059669",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._activar_docker,
        )
        self._btn_activar.pack(side="left", padx=(0, 10))

        self._btn_continuar = ctk.CTkButton(
            self._btn_row,
            text="Continuar sin Docker",
            width=210, height=46,
            fg_color=("gray78", "#334155"),
            hover_color=("gray68", "#475569"),
            font=ctk.CTkFont(size=15),
            command=self.on_ready,
        )
        self._btn_continuar.pack(side="left")

        ctk.CTkFrame(self, fg_color="transparent").pack(expand=True)

    # ── Verificación inicial ──────────────────────────────────────────
    def _verificar(self):
        docker_ok = self.docker_manager._ping()
        self.after(0, lambda: self._mostrar_resultado(docker_ok))

    def _mostrar_resultado(self, docker_ok: bool):
        self._bar.stop()
        self._bar.pack_forget()

        if docker_ok:
            self._badge.configure(fg_color=("#d1fae5", "#064e3b"))
            self._badge_lbl.configure(text="✓  Activo", text_color=C["ok"])
            self.after(1000, self.on_ready)
        else:
            self._badge.configure(fg_color=("#fef3c7", "#451a03"))
            self._badge_lbl.configure(text="✗  No disponible", text_color=C["warn"])
            self._warn_lbl.configure(
                text=(
                    "Docker no está instalado o no se encuentra en ejecución.\n"
                    "Sin Docker no podrás acceder a la sección de Laboratorios, "
                    "pero el resto de la aplicación funcionará con normalidad."
                )
            )
            self._btn_row.pack()

    # ── Activar Docker ────────────────────────────────────────────────
    def _activar_docker(self):
        if self._activando:
            return
        self._activando = True

        self._btn_activar.configure(state="disabled", text="Iniciando...")
        self._btn_continuar.configure(state="disabled")

        # Spinner mientras espera
        self._bar.pack(before=self._btn_row, pady=(0, 20))
        self._bar.start()

        threading.Thread(target=self._tarea_activar, daemon=True).start()

    def _tarea_activar(self):
        ok = self.docker_manager.iniciar_docker_desktop()
        self.after(0, lambda: self._tras_activar(ok))

    def _tras_activar(self, ok: bool):
        self._bar.stop()
        self._bar.pack_forget()
        self._activando = False

        if ok:
            self._badge.configure(fg_color=("#d1fae5", "#064e3b"))
            self._badge_lbl.configure(text="✓  Activo", text_color=C["ok"])
            self._warn_lbl.configure(text="")
            self._btn_row.pack_forget()
            self.after(800, self.on_ready)
        else:
            self._badge.configure(fg_color=("#fee2e2", "#450a0a"))
            self._badge_lbl.configure(text="✗  Error", text_color="#ef4444")
            self._warn_lbl.configure(
                text=(
                    "No se pudo iniciar Docker Desktop. Asegúrate de que esté instalado "
                    "y vuelve a intentarlo, o continúa sin acceso a Laboratorios."
                ),
                text_color="#ef4444",
            )
            self._btn_activar.configure(state="normal", text="Reintentar")
            self._btn_continuar.configure(state="normal")
