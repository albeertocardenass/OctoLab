import customtkinter as ctk
from utils.crypto import generar_codigo_hex

TEMAS = [
    {
        "id": 1,
        "titulo": "Reconocimiento con Nmap",
        "preguntas": [
            {"p": "¿Qué flag de nmap escanea todos los puertos?",  "opciones": ["-sV", "-p-", "-A", "-O"],                      "r": 1},
            {"p": "¿Qué significa el estado 'open' en nmap?",       "opciones": ["Filtrado", "Cerrado", "Accesible", "Desconocido"], "r": 2},
            {"p": "¿Para qué sirve -sV?",                           "opciones": ["Velocidad", "Detectar versiones", "Silencioso", "IPv6"], "r": 1},
        ]
    },
    {
        "id": 2,
        "titulo": "Explotación con Metasploit",
        "preguntas": [
            {"p": "¿Comando para buscar módulos en Metasploit?",    "opciones": ["find", "search", "list", "scan"],              "r": 1},
            {"p": "¿Qué hace 'use' en msfconsole?",                 "opciones": ["Sale", "Lista", "Selecciona módulo", "Ejecuta"], "r": 2},
            {"p": "¿Payload que da shell interactiva?",             "opciones": ["bind_tcp", "meterpreter", "reverse_http", "staged"], "r": 1},
        ]
    },
]

class TemarioScreen(ctk.CTkFrame):
    def __init__(self, master, usuario: dict, api_client):
        super().__init__(master, fg_color="transparent")
        self.usuario    = usuario
        self.api_client = api_client
        self.tema_idx   = 0
        self.preg_idx   = 0
        self.correctas  = 0
        self.modo       = "lista"   # "lista" | "test" | "resultado"
        self._mostrar_lista()

    # -- LISTA DE TEMAS -------------------------------------------
    def _mostrar_lista(self):
        self._limpiar()
        self.modo = "lista"
        ctk.CTkLabel(self, text="Temario", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 16))

        for i, tema in enumerate(TEMAS):
            btn = ctk.CTkButton(
                self, text=f"  {tema['titulo']}", anchor="w",
                width=500, height=50, corner_radius=10,
                fg_color="#1e293b", hover_color="#4f46e5",
                command=lambda idx=i: self._iniciar_test(idx)
            )
            btn.pack(pady=6)

    # -- TEST -----------------------------------------------------
    def _iniciar_test(self, idx: int):
        self.tema_idx  = idx
        self.preg_idx  = 0
        self.correctas = 0
        self.modo      = "test"
        self._mostrar_pregunta()

    def _mostrar_pregunta(self):
        self._limpiar()
        tema  = TEMAS[self.tema_idx]
        preg  = tema["preguntas"][self.preg_idx]
        total = len(tema["preguntas"])

        ctk.CTkLabel(self, text=tema["titulo"],
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 4))
        ctk.CTkLabel(self, text=f"Pregunta {self.preg_idx + 1} de {total}",
                     text_color="gray").pack(pady=(0, 20))
        ctk.CTkLabel(self, text=preg["p"],
                     font=ctk.CTkFont(size=15), wraplength=560).pack(pady=10)

        for i, opcion in enumerate(preg["opciones"]):
            ctk.CTkButton(
                self, text=opcion, width=400, height=44,
                fg_color="#1e293b", hover_color="#4f46e5",
                command=lambda idx=i: self._responder(idx)
            ).pack(pady=5)

    def _responder(self, idx: int):
        preg = TEMAS[self.tema_idx]["preguntas"][self.preg_idx]
        if idx == preg["r"]:
            self.correctas += 1
        self.preg_idx += 1
        total = len(TEMAS[self.tema_idx]["preguntas"])
        if self.preg_idx >= total:
            self._mostrar_resultado()
        else:
            self._mostrar_pregunta()

    # -- RESULTADO ------------------------------------------------
    def _mostrar_resultado(self):
        self._limpiar()
        tema     = TEMAS[self.tema_idx]
        total    = len(tema["preguntas"])
        aprobado = self.correctas >= (total // 2 + 1)

        ctk.CTkLabel(self,
                     text="✅ Test completado" if aprobado else "❌ No superado",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#10b981" if aprobado else "#ef4444").pack(pady=(40, 10))

        ctk.CTkLabel(self, text=f"{self.correctas}/{total} correctas",
                     font=ctk.CTkFont(size=16), text_color="gray").pack(pady=6)

        if aprobado:
            uid  = self.usuario.get("id", 0)
            code = generar_codigo_hex(uid, tema["id"])
            ctk.CTkLabel(self, text="Tu código para la web:",
                         font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(20, 4))
            code_box = ctk.CTkEntry(self, width=300, height=42,
                                     font=ctk.CTkFont(family="Courier New", size=16))
            code_box.insert(0, code)
            code_box.configure(state="readonly")
            code_box.pack(pady=4)
            ctk.CTkLabel(self, text="Introdúcelo en OctolabWeb para obtener tus puntos.",
                         text_color="gray", font=ctk.CTkFont(size=11)).pack(pady=4)

        ctk.CTkButton(self, text="Volver al temario", width=300,
                       fg_color="#4f46e5", hover_color="#4338ca",
                       command=self._mostrar_lista).pack(pady=30)

    def _limpiar(self):
        for w in self.winfo_children():
            w.destroy()
