import customtkinter as ctk
import json
import ctypes
import ctypes.wintypes
from config import APP_VERSION, THEME_FILE

# Tuplas (modo_claro, modo_oscuro)
C = {
    "primary":    "#4f46e5",
    "card":       ("gray92", "#1e293b"),
    "muted":      ("gray40", "#94a3b8"),
    "error":      "#ef4444",
    "divider":    ("gray80", "#334155"),
}

def _dwm_transitions(hwnd, enable: bool):
    """Activa o desactiva las animaciones DWM de la ventana."""
    try:
        val = ctypes.c_int(0 if enable else 1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 3,  # DWMWA_TRANSITIONS_FORCEDISABLED
            ctypes.byref(val), ctypes.sizeof(val)
        )
    except Exception:
        pass


class ConfigScreen(ctk.CTkFrame):
    def __init__(self, master, usuario: dict, auth_manager, on_logout):
        super().__init__(master, fg_color="transparent")
        self.usuario      = usuario
        self.auth_manager = auth_manager
        self.on_logout    = on_logout
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Configuracion",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(
                         anchor="w", padx=40, pady=(28, 20))

        card = ctk.CTkFrame(self, corner_radius=12, fg_color=C["card"])
        card.pack(padx=40, fill="x")

        # ── Datos del usuario ────────────────────────────────────────
        nombre = self.usuario.get("nombre", "")
        email  = self.usuario.get("email",  "")
        rol    = self.usuario.get("rol",    "")

        datos = ctk.CTkFrame(card, fg_color="transparent")
        datos.pack(fill="x", padx=24, pady=(24, 0))
        ctk.CTkLabel(datos, text=nombre,
                     font=ctk.CTkFont(size=15, weight="bold"),
                     anchor="w").pack(anchor="w")
        ctk.CTkLabel(datos, text=email,
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=12),
                     anchor="w").pack(anchor="w")
        ctk.CTkLabel(datos, text=rol,
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=12),
                     anchor="w").pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(card, height=1, fg_color=C["divider"]).pack(fill="x", padx=20, pady=16)

        # ── Tema ─────────────────────────────────────────────────────
        tema_row = ctk.CTkFrame(card, fg_color="transparent")
        tema_row.pack(fill="x", padx=24, pady=(0, 4))
        ctk.CTkLabel(tema_row, text="Tema oscuro",
                     font=ctk.CTkFont(size=13)).pack(side="left")
        self.theme_switch = ctk.CTkSwitch(tema_row, text="",
                                           command=self._toggle_theme)
        self.theme_switch.pack(side="right")
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

        ctk.CTkFrame(card, height=1, fg_color=C["divider"]).pack(fill="x", padx=20, pady=16)

        # ── Versión ──────────────────────────────────────────────────
        ctk.CTkLabel(card, text=f"Versión {APP_VERSION}",
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=11)).pack(pady=(0, 12))

        # ── Cerrar sesión ────────────────────────────────────────────
        ctk.CTkButton(card, text="Cerrar Sesion",
                       height=42,
                       fg_color=C["error"], hover_color="#dc2626",
                       command=self._logout).pack(padx=24, pady=(0, 24), fill="x")

    def _toggle_theme(self):
        modo = "Dark" if self.theme_switch.get() else "Light"
        root = self.winfo_toplevel()
        hwnd = root.winfo_id()

        # 1. Desactivar animaciones DWM para que el withdraw/deiconify interno
        #    de CTK no muestre la animación de apertura de Windows
        _dwm_transitions(hwnd, enable=False)

        # 2. Cambiar el tema
        ctk.set_appearance_mode(modo)

        # 3. Asegurar que la ventana está visible (CTK puede haberla ocultado)
        root.deiconify()
        root.lift()
        root.focus_force()

        # 4. Reactivar animaciones DWM tras un frame
        root.after(100, lambda: _dwm_transitions(hwnd, enable=True))

        try:
            with open(THEME_FILE, "w") as f:
                json.dump({"tema": modo}, f)
        except Exception:
            pass

    def _logout(self):
        self.auth_manager.cerrar_sesion()
        self.on_logout()
