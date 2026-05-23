import customtkinter as ctk
import threading

class DependencyScreen(ctk.CTkFrame):
    def __init__(self, master, docker_manager, on_ready):
        super().__init__(master, fg_color="transparent")
        self.docker_manager = docker_manager
        self.on_ready = on_ready
        self._build()
        threading.Thread(target=self._verificar, daemon=True).start()

    def _build(self):
        ctk.CTkLabel(self, text="Preparando el entorno",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(80, 10))
        self.status = ctk.StringVar(value="Comprobando Docker...")
        ctk.CTkLabel(self, textvariable=self.status,
                     text_color="gray", font=ctk.CTkFont(size=13)).pack(pady=6)
        self.bar = ctk.CTkProgressBar(self, width=400, mode="indeterminate")
        self.bar.pack(pady=20)
        self.bar.start()

    def _set_status(self, msg: str):
        self.after(0, lambda: self.status.set(msg))

    def _verificar(self):
        self._set_status("Iniciando Docker Desktop...")
        ok = self.docker_manager.iniciar_docker_desktop()
        if not ok:
            self._set_status("❌ No se pudo iniciar Docker. Instálalo y vuelve a intentarlo.")
            return

        self._set_status("Lanzando Kali y Metasploitable...")
        self.docker_manager.lanzar_labs(callback=self._set_status)
        self._set_status("✅ Entorno listo.")
        self.after(1000, self.on_ready)
