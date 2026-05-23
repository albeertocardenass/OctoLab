import customtkinter as ctk
import threading
from config import KALI_CONTAINER, META_CONTAINER

class LabsScreen(ctk.CTkFrame):
    def __init__(self, master, docker_manager):
        super().__init__(master, fg_color="transparent")
        self.docker_manager = docker_manager
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Laboratorios",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))

        self.vm_var = ctk.StringVar(value=KALI_CONTAINER)
        selector = ctk.CTkFrame(self, fg_color="transparent")
        selector.pack(pady=6)
        ctk.CTkRadioButton(selector, text="Kali Linux",
                           variable=self.vm_var, value=KALI_CONTAINER,
                           command=self._conectar).pack(side="left", padx=20)
        ctk.CTkRadioButton(selector, text="Metasploitable",
                           variable=self.vm_var, value=META_CONTAINER,
                           command=self._conectar).pack(side="left", padx=20)

        self.terminal = ctk.CTkTextbox(self, font=("Courier New", 12),
                                        fg_color="#0d1117", text_color="#c9d1d9",
                                        wrap="word")
        self.terminal.pack(fill="both", expand=True, padx=20, pady=10)

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.cmd_var = ctk.StringVar()
        entry = ctk.CTkEntry(input_frame, textvariable=self.cmd_var,
                              placeholder_text="Escribe un comando...",
                              fg_color="#161b22", height=40)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        entry.bind("<Return>", lambda e: self._enviar_cmd())

        ctk.CTkButton(input_frame, text="Enviar", width=100,
                       fg_color="#4f46e5", hover_color="#4338ca",
                       command=self._enviar_cmd).pack(side="right")

        self._conectar()

    def _conectar(self):
        self.terminal.delete("1.0", "end")
        vm = self.vm_var.get()
        estado = self.docker_manager.estado_contenedor(vm)
        self._escribir(f"[OctoLab] Conectado a {vm} (estado: {estado})\n$ ")

    def _enviar_cmd(self):
        cmd = self.cmd_var.get().strip()
        if not cmd:
            return
        self.cmd_var.set("")
        self._escribir(f"{cmd}\n")
        threading.Thread(target=self._ejecutar, args=(cmd,), daemon=True).start()

    def _ejecutar(self, cmd: str):
        salida = self.docker_manager.exec_comando(self.vm_var.get(), cmd)
        self.after(0, lambda: self._escribir(salida + "\n$ "))

    def _escribir(self, texto: str):
        self.terminal.insert("end", texto)
        self.terminal.see("end")
