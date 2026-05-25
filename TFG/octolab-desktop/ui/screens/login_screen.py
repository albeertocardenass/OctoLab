import customtkinter as ctk
import tkinter as tk
import math
import random
import webbrowser
from PIL import Image
from config import WEB_BASE_URL, IMAGES_DIR
import os

# ── Configuración de la animación ──────────────────────────────────
NUM_NODES    = 32
NODE_SPEED   = 0.45
CONNECT_DIST = 155
BG_COLOR     = "#0f172a"
NODE_COLOR   = "#4f46e5"
NODE_OUTLINE = "#6366f1"
LINE_BASE    = (0x31, 0x2e, 0x81)
NODE_R       = 2.5


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, on_login, on_guest=None):
        super().__init__(master, fg_color=BG_COLOR)
        self.on_login  = on_login
        self.on_guest  = on_guest
        self._nodes    = []
        self._running  = True
        self._show_pw  = False
        self._build()
        self.after(80, self._init_nodes)

    def destroy(self):
        self._running = False
        super().destroy()

    # ── UI ─────────────────────────────────────────────────────────
    def _build(self):
        # Canvas de fondo animado
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Contenedor central sobre el canvas
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        # ── Logo ────────────────────────────────────────────────────
        logo_row = ctk.CTkFrame(outer, fg_color="transparent")
        logo_row.pack(pady=(0, 6))

        # Cargar icono .ico con PIL
        _logo_img = None
        _ico_path = os.path.join(IMAGES_DIR, "octolab.ico")
        if os.path.exists(_ico_path):
            try:
                pil_img  = Image.open(_ico_path)
                # Tomar la variante de mayor resolución disponible
                sizes = getattr(pil_img, "ico", None)
                pil_img = pil_img.convert("RGBA").resize((48, 48), Image.LANCZOS)
                _logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(48, 48))
            except Exception:
                _logo_img = None

        if _logo_img:
            ctk.CTkLabel(logo_row, image=_logo_img, text="").pack(side="left")
        else:
            # Fallback: pastilla morada con letra O
            icon_box = ctk.CTkFrame(logo_row, width=48, height=48,
                                    corner_radius=10, fg_color="#4f46e5")
            icon_box.pack(side="left")
            icon_box.pack_propagate(False)
            ctk.CTkLabel(icon_box, text="O",
                         font=ctk.CTkFont(size=22, weight="bold"),
                         text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(logo_row, text="OctoLab",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color="white").pack(side="left", padx=(10, 0))

        # ── Subtítulo + Título ──────────────────────────────────────
        ctk.CTkLabel(outer, text="Bienvenido de nuevo",
                     font=ctk.CTkFont(size=13),
                     text_color="#64748b").pack(pady=(10, 2))

        ctk.CTkLabel(outer, text="Inicia sesión en OctoLab",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="white").pack(pady=(0, 22))

        # ── Tarjeta ─────────────────────────────────────────────────
        card = ctk.CTkFrame(outer, corner_radius=16,
                             fg_color="#1e293b",
                             border_width=1,
                             border_color="#334155")
        card.pack()

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=32, pady=28)

        self.email_var = ctk.StringVar()
        self.pass_var  = ctk.StringVar()
        self.error_var = ctk.StringVar()

        # ── Campo Email ─────────────────────────────────────────────
        ctk.CTkLabel(inner, text="Email",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#cbd5e1",
                     anchor="w").pack(anchor="w", pady=(0, 4))

        email_entry = ctk.CTkEntry(inner,
                                    placeholder_text="tu@email.com",
                                    textvariable=self.email_var,
                                    width=320, height=42,
                                    border_color="#334155",
                                    fg_color="#0f172a",
                                    text_color="white",
                                    placeholder_text_color="#475569")
        email_entry.pack()

        # ── Campo Contraseña ────────────────────────────────────────
        ctk.CTkLabel(inner, text="Contraseña",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#cbd5e1",
                     anchor="w").pack(anchor="w", pady=(16, 4))

        pw_row = ctk.CTkFrame(inner, fg_color="transparent")
        pw_row.pack()

        self.pass_entry = ctk.CTkEntry(pw_row,
                                        placeholder_text="••••••••",
                                        textvariable=self.pass_var,
                                        show="*",
                                        width=260, height=42,
                                        border_color="#334155",
                                        fg_color="#0f172a",
                                        text_color="white",
                                        placeholder_text_color="#475569")
        self.pass_entry.pack(side="left")

        self.toggle_btn = ctk.CTkButton(pw_row,
                                         text="Ver",
                                         width=54, height=42,
                                         fg_color="#1e3a5f",
                                         hover_color="#1e4a7f",
                                         text_color="#94a3b8",
                                         font=ctk.CTkFont(size=12),
                                         corner_radius=8,
                                         command=self._toggle_pw)
        self.toggle_btn.pack(side="left", padx=(4, 0))

        # ── Error ───────────────────────────────────────────────────
        ctk.CTkLabel(inner, textvariable=self.error_var,
                     text_color="#ef4444",
                     font=ctk.CTkFont(size=12),
                     anchor="w").pack(anchor="w", pady=(8, 0))

        # ── Botón Entrar ────────────────────────────────────────────
        self.btn = ctk.CTkButton(inner, text="Entrar",
                                  width=320, height=42,
                                  fg_color="#4f46e5",
                                  hover_color="#4338ca",
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  command=self._login)
        self.btn.pack(pady=(12, 0))

        # ── Botón Invitado ──────────────────────────────────────────
        ctk.CTkButton(inner, text="Entrar como Invitado",
                       width=320, height=42,
                       fg_color="transparent",
                       hover_color="#1e293b",
                       border_width=1,
                       border_color="#4f46e5",
                       text_color="#818cf8",
                       font=ctk.CTkFont(size=13),
                       command=self._guest_login).pack(pady=(8, 0))

        # ── Link de registro ─────────────────────────────────────────
        reg_row = ctk.CTkFrame(inner, fg_color="transparent")
        reg_row.pack(pady=(16, 0))
        ctk.CTkLabel(reg_row, text="¿No tienes cuenta? ",
                     font=ctk.CTkFont(size=12),
                     text_color="#64748b").pack(side="left")
        link = ctk.CTkLabel(reg_row, text="Regístrate aquí",
                             font=ctk.CTkFont(size=12, underline=True),
                             text_color="#818cf8",
                             cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda _: self._abrir_registro())

        # ── Atajos de teclado ────────────────────────────────────────
        email_entry.bind("<Return>", lambda _: self.pass_entry.focus())
        self.pass_entry.bind("<Return>", lambda _: self._login())

        # Foco inicial
        self.after(150, email_entry.focus)

        # Redimensionado
        self.bind("<Configure>", self._on_resize)

    # ── Toggle contraseña ───────────────────────────────────────────
    def _toggle_pw(self):
        self._show_pw = not self._show_pw
        self.pass_entry.configure(show="" if self._show_pw else "*")
        self.toggle_btn.configure(text="Ocultar" if self._show_pw else "Ver")

    # ── Redimensionado ──────────────────────────────────────────────
    def _on_resize(self, event):
        new_w, new_h = event.width, event.height
        old_w = getattr(self, "_canvas_w", 0)
        old_h = getattr(self, "_canvas_h", 0)
        if self._nodes and old_w > 0 and old_h > 0 and (old_w != new_w or old_h != new_h):
            sx = new_w / old_w
            sy = new_h / old_h
            for n in self._nodes:
                n["x"] *= sx
                n["y"] *= sy
        self._canvas_w = new_w
        self._canvas_h = new_h

    # ── Animación de nodos ──────────────────────────────────────────
    def _init_nodes(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10:
            self.after(50, self._init_nodes)
            return
        self._canvas_w = w
        self._canvas_h = h
        self._nodes = [
            {
                "x":  random.uniform(0, w),
                "y":  random.uniform(0, h),
                "vx": random.choice([-1, 1]) * random.uniform(0.2, NODE_SPEED),
                "vy": random.choice([-1, 1]) * random.uniform(0.2, NODE_SPEED),
            }
            for _ in range(NUM_NODES)
        ]
        self._animate()

    def _animate(self):
        if not self._running:
            return
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10:
            self.after(33, self._animate)
            return

        self.canvas.delete("all")

        for n in self._nodes:
            n["x"] += n["vx"]
            n["y"] += n["vy"]
            if not (0 <= n["x"] <= w):
                n["vx"] *= -1
            if not (0 <= n["y"] <= h):
                n["vy"] *= -1

        for i, a in enumerate(self._nodes):
            for b in self._nodes[i + 1:]:
                dist = math.hypot(a["x"] - b["x"], a["y"] - b["y"])
                if dist < CONNECT_DIST:
                    factor = 1 - dist / CONNECT_DIST
                    r   = min(int(LINE_BASE[0] + 80 * factor), 255)
                    g   = min(int(LINE_BASE[1] + 40 * factor), 255)
                    b_c = min(int(LINE_BASE[2] + 60 * factor), 255)
                    self.canvas.create_line(
                        a["x"], a["y"], b["x"], b["y"],
                        fill=f"#{r:02x}{g:02x}{b_c:02x}",
                        width=1
                    )

        for n in self._nodes:
            x, y = n["x"], n["y"]
            self.canvas.create_oval(
                x - NODE_R, y - NODE_R,
                x + NODE_R, y + NODE_R,
                fill=NODE_COLOR, outline=NODE_OUTLINE, width=1
            )

        self.after(33, self._animate)

    # ── Acciones ────────────────────────────────────────────────────
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

    def _guest_login(self):
        if self.on_guest:
            self.on_guest()

    def _abrir_registro(self):
        webbrowser.open(f"{WEB_BASE_URL}/register")
