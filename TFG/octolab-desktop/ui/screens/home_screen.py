"""
home_screen.py — Pantalla de inicio: bienvenida, resumen de funciones y créditos del proyecto.
"""
import base64
import io
import customtkinter as ctk
from PIL import Image, ImageDraw

C = {
    "primary":     "#4f46e5",
    "primary_hov": "#4338ca",
    "card":        ("white", "#1e293b"),
    "muted":       ("gray40", "#94a3b8"),
    "success":     "#10b981",
    "divider":     ("gray80", "#334155"),
    "tag_bg":      ("gray88", "#334155"),
    "avatar2":     ("#e0e7ff", "#312e81"),
}

SIZE_AVATAR = 72


def _avatar_desde_base64(b64: str) -> ctk.CTkImage | None:
    """Convierte una cadena base64 en un CTkImage circular."""
    try:
        if "," in b64:
            b64 = b64.split(",", 1)[1]
        data   = base64.b64decode(b64)
        img    = Image.open(io.BytesIO(data)).convert("RGBA")
        img    = img.resize((SIZE_AVATAR, SIZE_AVATAR), Image.LANCZOS)
        mask   = Image.new("L", (SIZE_AVATAR, SIZE_AVATAR), 0)
        draw   = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, SIZE_AVATAR, SIZE_AVATAR), fill=255)
        result = Image.new("RGBA", (SIZE_AVATAR, SIZE_AVATAR), (0, 0, 0, 0))
        result.paste(img, mask=mask)
        return ctk.CTkImage(light_image=result, dark_image=result,
                            size=(SIZE_AVATAR, SIZE_AVATAR))
    except Exception:
        return None



FEATURES = [
    (
        "TM", "#4f46e5", "Temario",
        "12 módulos de ciberseguridad: fundamentos, redes, ethical hacking, criptografía, "
        "seguridad en la nube y más. Desbloquea cada tema con puntos Octo.",
    ),
    (
        "LB", "#0891b2", "Laboratorios",
        "Arranca contenedores Docker con Kali Linux y Metasploitable 2 interconectados en red. "
        "Abre una terminal directa desde la app y practica en un entorno real.",
    ),
    (
        "TS", "#059669", "Tests y Códigos",
        "Completa el test de 10 preguntas de cada módulo. Con ≥ 7 / 10 recibes un código "
        "hexadecimal único que validas en la web para registrar tu progreso.",
    ),
    (
        "CF", "#7c3aed", "Configuración",
        "Alterna entre tema oscuro y claro sin reiniciar la aplicación. Consulta tu perfil, "
        "rol y puntos, y cierra sesión de forma segura.",
    ),
]

ABOUT = (
    "OctoLab es un Trabajo de Fin de Grado (TFG) orientado a la formación práctica en "
    "ciberseguridad. La plataforma combina contenidos teóricos, entornos de laboratorio "
    "Docker y un sistema de gamificación con puntos Octo para motivar el aprendizaje "
    "progresivo y autodirigido.\n\n"
    "Desarrollada como ecosistema completo: aplicación de escritorio en Python "
    "(customtkinter), aplicación web en Angular y API REST en ASP.NET Core."
)

AUTORES = [
    (
        "Alberto Cárdenas Palomo",
        "Desarrollador Full Stack",
        "Responsable de la aplicación de escritorio Python, la infraestructura\n"
        "Docker con red NAT para los laboratorios, y co-desarrollador de la\n"
        "plataforma web Angular y la API ASP.NET Core.",
        ["Angular", "ASP.NET Core", "Python", "Docker", "TypeScript", "C#"],
    ),
    (
        "Juan Alberto Campaña Espejo",
        "Desarrollador Full Stack",
        "Responsable del despliegue en AWS (EC2, S3, RDS, Terraform) y la base\n"
        "de datos MySQL, y co-desarrollador de la plataforma web Angular y la\n"
        "API ASP.NET Core.",
        ["Angular", "ASP.NET Core", "AWS", "TypeScript", "C#", "MySQL", "Terraform"],
    ),
]




class HomeScreen(ctk.CTkFrame):
    def __init__(self, master, usuario: dict, api_client=None):
        super().__init__(master, fg_color="transparent")
        self.usuario = usuario
        self._build()


    def _build(self):
        nombre          = self.usuario.get("nombre", "Usuario")
        rol             = self.usuario.get("rol",    "Usuario")
        puntos          = self.usuario.get("puntos", 0)
        inicial         = nombre[0].upper() if nombre else "U"
        avatar_b64      = self.usuario.get("avatar", "")
        desbloqueados   = self.usuario.get("modulosDesbloqueados", [])
        n_desbloqueados = len(desbloqueados)


        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)


        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(24, 14))

        img_ctk = (
            _avatar_desde_base64(avatar_b64)
            if avatar_b64 and avatar_b64.startswith("data:")
            else None
        )
        if img_ctk:
            ctk.CTkLabel(header, image=img_ctk, text="").pack(side="left")
        else:
            av = ctk.CTkFrame(
                header, width=SIZE_AVATAR, height=SIZE_AVATAR,
                corner_radius=SIZE_AVATAR // 2, fg_color=C["primary"],
            )
            av.pack(side="left")
            av.pack_propagate(False)
            ctk.CTkLabel(
                av, text=inicial,
                font=ctk.CTkFont(size=30, weight="bold"),
                text_color="white",
            ).place(relx=0.5, rely=0.5, anchor="center")

        info = ctk.CTkFrame(header, fg_color="transparent")
        info.pack(side="left", padx=16)
        ctk.CTkLabel(
            info, text=f"Bienvenido, {nombre}",
            font=ctk.CTkFont(size=28, weight="bold"),
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text=f"{rol}  •  {puntos} Puntos Octo",
            text_color=C["muted"],
            font=ctk.CTkFont(size=16),
            anchor="w",
        ).pack(anchor="w")


        prog = ctk.CTkFrame(scroll, fg_color="transparent")
        prog.pack(fill="x", padx=40, pady=(0, 6))

        ctk.CTkLabel(
            prog, text="Progreso del Temario",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=C["muted"],
        ).pack(anchor="w", pady=(0, 4))

        bar = ctk.CTkProgressBar(prog, height=8, progress_color=C["primary"])
        bar.set(n_desbloqueados / 12)
        bar.pack(fill="x")

        ctk.CTkLabel(
            prog,
            text=f"{n_desbloqueados} / 12 módulos desbloqueados",
            text_color=C["muted"],
            font=ctk.CTkFont(size=14),
        ).pack(anchor="w", pady=(4, 0))


        ctk.CTkFrame(scroll, height=1, fg_color=C["divider"]).pack(
            fill="x", padx=40, pady=(14, 14))


        ctk.CTkLabel(
            scroll, text="¿Qué ofrece OctoLab?",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=40, pady=(0, 10))

        feat_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        feat_grid.pack(fill="x", padx=40, pady=(0, 6))
        feat_grid.grid_columnconfigure((0, 1), weight=1, uniform="feat")

        for i, (abrev, color, titulo, desc) in enumerate(FEATURES):
            card = ctk.CTkFrame(
                feat_grid, corner_radius=12,
                fg_color=C["card"],
                border_width=1, border_color=C["divider"],
            )
            card.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="nsew")

            inn = ctk.CTkFrame(card, fg_color="transparent")
            inn.pack(fill="both", expand=True, padx=16, pady=14)


            accent = ctk.CTkFrame(inn, width=3, corner_radius=2, fg_color=color)
            accent.pack(side="left", fill="y", padx=(0, 12))
            accent.pack_propagate(False)

            body = ctk.CTkFrame(inn, fg_color="transparent")
            body.pack(side="left", fill="both", expand=True)


            top_row = ctk.CTkFrame(body, fg_color="transparent")
            top_row.pack(anchor="w", pady=(0, 7))

            bdg = ctk.CTkFrame(top_row, width=38, height=24,
                               corner_radius=5, fg_color=color)
            bdg.pack(side="left")
            bdg.pack_propagate(False)
            ctk.CTkLabel(
                bdg, text=abrev,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
            ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                top_row, text=titulo,
                font=ctk.CTkFont(size=16, weight="bold"),
            ).pack(side="left", padx=(8, 0))

            ctk.CTkLabel(
                body, text=desc,
                text_color=C["muted"],
                font=ctk.CTkFont(size=14),
                anchor="w", justify="left",
                wraplength=255,
            ).pack(anchor="w")


        ctk.CTkFrame(scroll, height=1, fg_color=C["divider"]).pack(
            fill="x", padx=40, pady=(14, 14))


        ctk.CTkLabel(
            scroll, text="Sobre el proyecto",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=40, pady=(0, 8))

        ctk.CTkLabel(
            scroll, text=ABOUT,
            text_color=C["muted"],
            font=ctk.CTkFont(size=15),
            anchor="w", justify="left",
            wraplength=720,
        ).pack(anchor="w", padx=40, pady=(0, 18))


        ctk.CTkLabel(
            scroll, text="Equipo",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=40, pady=(0, 10))

        equipo_row = ctk.CTkFrame(scroll, fg_color="transparent")
        equipo_row.pack(anchor="w", padx=40, pady=(0, 28))

        for nombre_a, rol_a, desc_a, techs_a in AUTORES:
            initials = "".join(p[0] for p in nombre_a.split()[:2])
            card = ctk.CTkFrame(
                equipo_row, corner_radius=12,
                fg_color=C["card"],
                border_width=1, border_color=C["divider"],
            )
            card.pack(side="left", padx=(0, 14))

            inn = ctk.CTkFrame(card, fg_color="transparent")
            inn.pack(padx=20, pady=18)


            av2 = ctk.CTkFrame(inn, width=56, height=56,
                                corner_radius=28, fg_color=C["primary"])
            av2.pack(anchor="w", pady=(0, 10))
            av2.pack_propagate(False)
            ctk.CTkLabel(
                av2, text=initials,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="white",
            ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                inn, text=nombre_a,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w",
            ).pack(anchor="w")


            badge = ctk.CTkFrame(inn, fg_color=C["avatar2"], corner_radius=6)
            badge.pack(anchor="w", pady=(4, 6))
            ctk.CTkLabel(
                badge, text=rol_a.upper(),
                text_color=C["primary"],
                font=ctk.CTkFont(size=11, weight="bold"),
            ).pack(padx=8, pady=3)


            ctk.CTkLabel(
                inn, text=desc_a,
                text_color=C["muted"],
                font=ctk.CTkFont(size=13),
                anchor="w", justify="left",
            ).pack(anchor="w", pady=(0, 10))


            pills_row = ctk.CTkFrame(inn, fg_color="transparent")
            pills_row.pack(anchor="w")
            row1 = ctk.CTkFrame(pills_row, fg_color="transparent")
            row1.pack(anchor="w")
            row2 = ctk.CTkFrame(pills_row, fg_color="transparent")
            row2.pack(anchor="w", pady=(4, 0))
            for i, tech in enumerate(techs_a):
                target_row = row1 if i < 4 else row2
                pill = ctk.CTkFrame(target_row, fg_color=C["tag_bg"], corner_radius=6)
                pill.pack(side="left", padx=(0, 4))
                ctk.CTkLabel(
                    pill, text=tech,
                    font=ctk.CTkFont(size=12),
                    text_color=C["muted"],
                ).pack(padx=7, pady=3)
