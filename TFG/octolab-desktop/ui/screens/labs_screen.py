import customtkinter as ctk
import subprocess
import threading
from config import KALI_CONTAINER, META_CONTAINER, KALI_IMAGE, METASPLOITABLE_IMAGE, DOCKER_NETWORK

C = {
    "primary":     "#4f46e5",
    "primary_hov": "#4338ca",
    "card":        ("gray92", "#1e293b"),
    "muted":       ("gray40", "#94a3b8"),
    "success":     "#10b981",
    "error":       "#ef4444",
    "stopped":     ("gray60", "#64748b"),
    "divider":     ("gray80", "#334155"),
    "copy_ok":     "#10b981",
}

CONTENEDORES = [
    (KALI_CONTAINER,  KALI_IMAGE,           "Kali Linux",       "Distribución ofensiva para pentesting y auditorías"),
    (META_CONTAINER,  METASPLOITABLE_IMAGE,  "Metasploitable 2", "Máquina intencionalmente vulnerable para práctica"),
]

# ── Referencia de comandos ────────────────────────────────────────────
# (descripción, comando)
COMANDOS = {
    ("RE", "#0891b2", "Reconocimiento"): [
        ("Descubrir hosts en la red",             "nmap -sn 172.18.0.0/16"),
        ("Escaneo de servicios (puertos comunes)","nmap -sV -p 1-1000 <IP_objetivo>"),
        ("Escaneo completo de todos los puertos", "nmap -sV -p- <IP_objetivo>"),
        ("Escaneo con scripts NSE por defecto",   "nmap -sV -sC <IP_objetivo>"),
        ("Escaneo agresivo (OS + scripts)",        "nmap -A <IP_objetivo>"),
        ("Detectar vulnerabilidades conocidas",    "nmap --script vuln <IP_objetivo>"),
    ],
    ("MS", "#7c3aed", "Metasploit Framework"): [
        ("Iniciar el framework",                  "msfconsole"),
        ("Buscar módulos o exploits",             "search <término>"),
        ("Seleccionar un módulo",                 "use <ruta/del/módulo>"),
        ("Ver opciones del módulo activo",        "show options"),
        ("Configurar IP del objetivo",            "set RHOSTS <IP_objetivo>"),
        ("Configurar IP del atacante",            "set LHOST <IP_kali>"),
        ("Ejecutar el módulo",                    "run"),
        ("Listar sesiones activas",               "sessions -l"),
        ("Conectar a una sesión Meterpreter",     "sessions -i <ID>"),
    ],
    ("EX", "#dc2626", "Exploits — Metasploitable 2"): [
        ("vsftpd 2.3.4 backdoor  (puerto 21)",    "use exploit/unix/ftp/vsftpd_234_backdoor"),
        ("Samba usermap_script   (puerto 445)",   "use exploit/multi/samba/usermap_script"),
        ("DistCC exec            (puerto 3632)",  "use exploit/unix/misc/distcc_exec"),
        ("UnrealIRCd backdoor    (puerto 6667)",  "use exploit/unix/irc/unreal_ircd_3281_backdoor"),
        ("Tomcat manager upload  (puerto 8180)",  "use exploit/multi/http/tomcat_mgr_upload"),
        ("Fuerza bruta SSH",                      "use auxiliary/scanner/ssh/ssh_login"),
    ],
    ("PE", "#059669", "Post-explotación"): [
        ("Ver usuario actual",                    "whoami"),
        ("Ver UID / GID del usuario",             "id"),
        ("Información del sistema operativo",     "uname -a"),
        ("Obtener shell TTY interactiva",         "python -c 'import pty; pty.spawn(\"/bin/bash\")'"),
        ("Ver usuarios del sistema",              "cat /etc/passwd"),
        ("Buscar binarios SUID (escalada)",       "find / -perm -4000 2>/dev/null"),
    ],
    ("RD", "#4f46e5", "Red y Docker"): [
        ("IP de Metasploitable en la red interna",
         f"docker inspect -f '{{{{.NetworkSettings.Networks.{DOCKER_NETWORK}.IPAddress}}}}' {META_CONTAINER}"),
        ("IP de Kali en la red interna",
         f"docker inspect -f '{{{{.NetworkSettings.Networks.{DOCKER_NETWORK}.IPAddress}}}}' {KALI_CONTAINER}"),
        ("Comprobar conectividad con el objetivo","ping -c 4 <IP_objetivo>"),
    ],
}


# ── Botón icono ───────────────────────────────────────────────────────
def _icon_btn(parent, icon: str, label: str,
              fg, hover, command, enabled: bool = True) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn = ctk.CTkButton(
        frame, text=icon,
        width=48, height=44, corner_radius=10,
        fg_color=fg, hover_color=hover,
        font=ctk.CTkFont(size=17),
        state="normal" if enabled else "disabled",
        command=command,
    )
    btn.pack()
    ctk.CTkLabel(frame, text=label,
                 font=ctk.CTkFont(size=10),
                 text_color=C["muted"]).pack(pady=(3, 0))
    frame._btn = btn
    return frame


# ── Pantalla ──────────────────────────────────────────────────────────
class LabsScreen(ctk.CTkFrame):
    def __init__(self, master, docker_manager):
        super().__init__(master, fg_color="transparent")
        self.docker        = docker_manager
        self.estado_labels = {}
        self.ip_labels     = {}
        self._start_frames = {}
        self._term_frames  = {}
        self._stop_frames  = {}
        self._build()
        threading.Thread(target=self._refrescar_estados, daemon=True).start()

    # ── Construcción ─────────────────────────────────────────────────
    def _build(self):
        # Título fuera del scroll (cabecera fija)
        ctk.CTkLabel(self, text="Laboratorios",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(
                         anchor="w", padx=40, pady=(28, 2))
        ctk.CTkLabel(self,
                     text="Los contenedores comparten la red interna octolab-net — "
                          "Kali puede escanear y explotar Metasploitable directamente.",
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=12),
                     wraplength=660, justify="left").pack(anchor="w", padx=40, pady=(0, 16))

        ctk.CTkFrame(self, height=1, fg_color=C["divider"]).pack(fill="x", padx=40, pady=(0, 12))

        # Todo lo demás desplazable
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # ── Tarjetas de contenedores ──────────────────────────────────
        for nombre, imagen, titulo, desc in CONTENEDORES:
            card = ctk.CTkFrame(scroll, corner_radius=12, fg_color=C["card"])
            card.pack(fill="x", padx=40, pady=6)

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=20, pady=(14, 4))
            ctk.CTkLabel(top, text=titulo,
                         font=ctk.CTkFont(size=15, weight="bold")).pack(side="left")
            estado_lbl = ctk.CTkLabel(top, text="Detenido",
                                       text_color=C["stopped"],
                                       font=ctk.CTkFont(size=12, weight="bold"))
            estado_lbl.pack(side="right")
            self.estado_labels[nombre] = estado_lbl

            ctk.CTkLabel(card, text=desc,
                         text_color=C["muted"],
                         font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)

            ip_lbl = ctk.CTkLabel(card, text="",
                                   text_color=C["primary"],
                                   font=ctk.CTkFont(family="Courier New", size=11))
            ip_lbl.pack(anchor="w", padx=20, pady=(2, 0))
            self.ip_labels[nombre] = ip_lbl

            btns_row = ctk.CTkFrame(card, fg_color="transparent")
            btns_row.pack(anchor="w", padx=20, pady=(12, 16))

            start_f = _icon_btn(btns_row, "▶", "Iniciar",
                                 C["primary"], C["primary_hov"],
                                 lambda n=nombre, img=imagen: self._iniciar(n, img))
            start_f.pack(side="left", padx=(0, 10))
            self._start_frames[nombre] = start_f

            term_f = _icon_btn(btns_row, ">_", "Terminal",
                                ("#1e3a5f", "#1e3a5f"), "#1e4a7f",
                                lambda n=nombre: self._abrir_terminal(n),
                                enabled=False)
            term_f.pack(side="left", padx=(0, 10))
            self._term_frames[nombre] = term_f

            stop_f = _icon_btn(btns_row, "■", "Detener",
                                "#ef4444", "#dc2626",
                                lambda n=nombre: self._detener(n),
                                enabled=False)
            stop_f.pack(side="left")
            self._stop_frames[nombre] = stop_f

        # ── Referencia de comandos ────────────────────────────────────
        ctk.CTkFrame(scroll, height=1, fg_color=C["divider"]).pack(
            fill="x", padx=40, pady=(20, 16))

        ctk.CTkLabel(scroll, text="Referencia de comandos",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(
                         anchor="w", padx=40, pady=(0, 12))

        ctk.CTkLabel(scroll,
                     text="Comandos de uso frecuente en los laboratorios. "
                          "Haz clic en Copiar para llevarlos directamente a la terminal.",
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=11),
                     wraplength=660, justify="left").pack(anchor="w", padx=40, pady=(0, 14))

        for (abrev, color, categoria), cmds in COMANDOS.items():
            self._seccion_comandos(scroll, abrev, color, categoria, cmds)

        # Margen inferior
        ctk.CTkFrame(scroll, height=20, fg_color="transparent").pack()

    def _seccion_comandos(self, parent, abrev: str, color: str,
                          titulo: str, cmds: list):
        """Renderiza una categoría de comandos con su tarjeta."""
        # Cabecera de categoría
        hdr = ctk.CTkFrame(parent, fg_color="transparent")
        hdr.pack(fill="x", padx=40, pady=(0, 6))

        bdg = ctk.CTkFrame(hdr, width=32, height=22,
                           corner_radius=5, fg_color=color)
        bdg.pack(side="left")
        bdg.pack_propagate(False)
        ctk.CTkLabel(bdg, text=abrev,
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(hdr, text=titulo,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(
                         side="left", padx=(8, 0))

        # Tarjeta con filas de comandos
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color=C["card"])
        card.pack(fill="x", padx=40, pady=(0, 14))

        for j, (desc, cmd) in enumerate(cmds):
            if j > 0:
                ctk.CTkFrame(card, height=1, fg_color=C["divider"]).pack(
                    fill="x", padx=14)

            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=7)

            # Descripción
            ctk.CTkLabel(row, text=desc,
                         text_color=C["muted"],
                         font=ctk.CTkFont(size=11),
                         width=240, anchor="w").pack(side="left")

            # Comando en monospace
            ctk.CTkLabel(row, text=cmd,
                         font=ctk.CTkFont(family="Courier New", size=11),
                         anchor="w").pack(side="left", fill="x", expand=True, padx=(8, 8))

            # Botón copiar
            copy_btn = ctk.CTkButton(
                row, text="Copiar",
                width=64, height=26,
                corner_radius=6,
                fg_color=("gray78", "#334155"),
                hover_color=("gray68", "#475569"),
                font=ctk.CTkFont(size=10),
            )
            copy_btn.configure(
                command=lambda c=cmd, b=copy_btn: self._copiar(c, b))
            copy_btn.pack(side="right")

    # ── Estado de contenedores ────────────────────────────────────────
    def _refrescar_estados(self):
        for nombre, _, _, _ in CONTENEDORES:
            try:
                estado = self.docker.estado_contenedor(nombre)
                ip     = self.docker.get_ip_contenedor(nombre) if estado == "running" else None
                self.after(0, lambda n=nombre, e=estado, i=ip: self._set_estado(n, e, i))
            except Exception:
                pass

    def _set_estado(self, nombre: str, estado: str, ip: str | None = None):
        lbl     = self.estado_labels.get(nombre)
        ip_lbl  = self.ip_labels.get(nombre)
        running = estado == "running"

        if lbl:
            if running:
                lbl.configure(text="En ejecucion", text_color=C["success"])
            elif estado == "error":
                lbl.configure(text="Error",        text_color=C["error"])
            else:
                lbl.configure(text="Detenido",     text_color=C["stopped"])

        if ip_lbl:
            ip_lbl.configure(text=f"IP red interna: {ip}" if ip else "")

        self._set_btn_enabled(self._start_frames.get(nombre), not running)
        self._set_btn_enabled(self._term_frames.get(nombre),  running)
        self._set_btn_enabled(self._stop_frames.get(nombre),  running)

    @staticmethod
    def _set_btn_enabled(frame, enabled: bool):
        if frame and hasattr(frame, "_btn"):
            frame._btn.configure(state="normal" if enabled else "disabled")

    # ── Acciones ─────────────────────────────────────────────────────
    def _iniciar(self, nombre: str, imagen: str):
        def tarea():
            self.after(0, lambda: self.estado_labels[nombre].configure(
                text="Iniciando...", text_color=C["muted"]))
            self.after(0, lambda: [
                self._set_btn_enabled(self._start_frames.get(nombre), False),
                self._set_btn_enabled(self._term_frames.get(nombre),  False),
                self._set_btn_enabled(self._stop_frames.get(nombre),  False),
            ])
            ok = self.docker.lanzar_contenedor(nombre, imagen)
            ip = self.docker.get_ip_contenedor(nombre) if ok else None
            self.after(0, lambda: self._set_estado(nombre, "running" if ok else "error", ip))
        threading.Thread(target=tarea, daemon=True).start()

    def _detener(self, nombre: str):
        def tarea():
            try:
                if self.docker.client:
                    self.docker.client.containers.get(nombre).stop()
                self.after(0, lambda: self._set_estado(nombre, "stopped"))
            except Exception:
                pass
        threading.Thread(target=tarea, daemon=True).start()

    def _abrir_terminal(self, nombre: str):
        try:
            subprocess.Popen(
                ["cmd.exe", "/k", f"docker exec -it {nombre} /bin/bash"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            print(f"Error abriendo terminal: {e}")

    def _copiar(self, cmd: str, btn: ctk.CTkButton):
        self.clipboard_clear()
        self.clipboard_append(cmd)
        self.update()
        btn.configure(text="✓", fg_color=C["copy_ok"], hover_color="#059669")
        self.after(1500, lambda: btn.configure(
            text="Copiar",
            fg_color=("gray78", "#334155"),
            hover_color=("gray68", "#475569"),
        ))
