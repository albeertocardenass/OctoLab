import os
import subprocess
import time
import docker
from config import (
    KALI_IMAGE, METASPLOITABLE_IMAGE,
    KALI_CONTAINER, META_CONTAINER, DOCKER_NETWORK, DOCKER_DIR
)
from utils.logger import get_logger

log = get_logger("docker_manager")

# Kali necesita NET_RAW + NET_ADMIN para nmap/ping y correr como root
# para que los binarios SUID no sean bloqueados por el kernel.
_CAPS: dict[str, list[str]] = {
    KALI_CONTAINER: ["NET_RAW", "NET_ADMIN"],
}
_USER: dict[str, str] = {
    KALI_CONTAINER: "root",
}


class DockerManager:
    def __init__(self):
        self.client = None

    # ── Conexión ─────────────────────────────────────────────────────
    def iniciar_docker_desktop(self) -> bool:
        import platform
        if platform.system() != "Windows":
            return self._ping()
        subprocess.Popen(
            r"C:\Program Files\Docker\Docker\Docker Desktop.exe",
            shell=True,
        )
        log.info("Esperando a que Docker arranque...")
        for _ in range(30):
            if self._ping():
                log.info("Docker listo.")
                return True
            time.sleep(2)
        return False

    def _ping(self) -> bool:
        try:
            self.client = docker.from_env()
            self.client.ping()
            return True
        except Exception:
            self.client = None
            return False

    def _ensure_client(self) -> bool:
        if self.client is not None:
            try:
                self.client.ping()
                return True
            except Exception:
                self.client = None
        return self._ping()

    # ── Imagen personalizada de Kali ─────────────────────────────────
    def _imagen_existe(self, imagen: str) -> bool:
        try:
            self.client.images.get(imagen)
            return True
        except (docker.errors.ImageNotFound, Exception):
            return False

    def construir_imagen_kali(self, on_status=None) -> bool:
        """
        Construye octolab-kali:latest usando el CLI de Docker (subprocess).
        Más robusto que el SDK Python para operaciones de build.
        """
        dockerfile = os.path.join(DOCKER_DIR, "Dockerfile.kali")
        if on_status:
            on_status("Construyendo imagen de Kali (primera vez ~3-5 min)...")
        log.info("Iniciando build de octolab-kali:latest...")
        try:
            proc = subprocess.Popen(
                [
                    "docker", "build",
                    "--no-cache",        # evita usar capas rotas de builds anteriores
                    "-t", KALI_IMAGE,
                    "-f", dockerfile,
                    DOCKER_DIR,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            for line in proc.stdout:
                line = line.strip()
                if not line:
                    continue
                log.info(f"[build] {line}")
                if on_status and ("Step" in line or "step" in line
                                  or "#" in line):
                    # Truncar a 50 chars para que quepa en la etiqueta
                    on_status(line[:50] + ("…" if len(line) > 50 else ""))

            proc.wait()
            if proc.returncode == 0:
                log.info("Imagen octolab-kali:latest construida correctamente.")
                return True
            else:
                # En Docker Desktop/Windows el pipe puede cerrarse con EOF
                # aunque la imagen se haya creado. Verificar antes de fallar.
                if self._imagen_existe(KALI_IMAGE):
                    log.info("Imagen construida correctamente (EOF de pipe ignorado).")
                    return True
                log.error(f"Build falló con código {proc.returncode}")
                if on_status:
                    on_status(f"Error: build falló (código {proc.returncode})")
                return False
        except FileNotFoundError:
            msg = "Docker CLI no encontrado en PATH"
            log.error(msg)
            if on_status:
                on_status(msg)
            return False
        except Exception as e:
            log.error(f"Error construyendo imagen Kali: {e}")
            if on_status:
                on_status(f"Error: {e}")
            return False

    # ── Red ───────────────────────────────────────────────────────────
    def crear_red(self):
        if not self._ensure_client():
            return
        try:
            self.client.networks.get(DOCKER_NETWORK)
        except docker.errors.NotFound:
            self.client.networks.create(DOCKER_NETWORK, driver="bridge")
            log.info(f"Red {DOCKER_NETWORK} creada.")
        except Exception as e:
            log.error(f"Error creando red: {e}")

    # ── Contenedores ─────────────────────────────────────────────────
    def lanzar_contenedor(self, nombre: str, imagen: str,
                          on_status=None) -> bool:
        if not self._ensure_client():
            log.error("Docker no disponible.")
            return False

        # Construir imagen custom de Kali si no existe todavía
        if nombre == KALI_CONTAINER and not self._imagen_existe(KALI_IMAGE):
            ok = self.construir_imagen_kali(on_status)
            if not ok:
                return False

        self.crear_red()

        caps = _CAPS.get(nombre, [])
        user = _USER.get(nombre, None)

        try:
            # ── Comprobar si ya existe el contenedor ─────────────────
            try:
                c = self.client.containers.get(nombre)
                existing_caps = c.attrs.get("HostConfig", {}).get("CapAdd") or []
                existing_user = c.attrs.get("Config", {}).get("User", "")
                caps_ok = not caps or all(cap in existing_caps for cap in caps)
                user_ok = not user or existing_user == user
                if not caps_ok or not user_ok:
                    log.info(f"{nombre}: reconfigurando contenedor...")
                    if on_status:
                        on_status(f"Reconfigurando {nombre}...")
                    if c.status == "running":
                        c.stop(timeout=5)
                    c.remove()
                    raise docker.errors.NotFound("reconfiguring")
                if c.status != "running":
                    c.start()
                    log.info(f"{nombre} reanudado.")
                return True
            except docker.errors.NotFound:
                pass

            # ── Crear contenedor nuevo ───────────────────────────────
            if on_status:
                on_status(f"Iniciando {nombre}...")

            run_kwargs: dict = dict(
                name=nombre,
                network=DOCKER_NETWORK,
                detach=True,
                tty=True,
                stdin_open=True,
            )
            if caps:
                run_kwargs["cap_add"] = caps
            if user:
                run_kwargs["user"] = user

            self.client.containers.run(imagen, **run_kwargs)
            log.info(f"{nombre} iniciado (caps={caps}, user={user}).")
            return True

        except Exception as e:
            log.error(f"Error lanzando {nombre}: {e}")
            if on_status:
                on_status(f"Error: {e}")
            return False

    # ── Utilidades ────────────────────────────────────────────────────
    def get_ip_contenedor(self, nombre: str) -> str | None:
        if not self._ensure_client():
            return None
        try:
            c = self.client.containers.get(nombre)
            redes = c.attrs.get("NetworkSettings", {}).get("Networks", {})
            ip = redes.get(DOCKER_NETWORK, {}).get("IPAddress")
            return ip or None
        except Exception:
            return None

    def estado_contenedor(self, nombre: str) -> str:
        if not self._ensure_client():
            return "stopped"
        try:
            return self.client.containers.get(nombre).status
        except Exception:
            return "stopped"

    def parar_labs(self):
        for nombre in [KALI_CONTAINER, META_CONTAINER]:
            try:
                self.client.containers.get(nombre).stop()
                log.info(f"{nombre} parado.")
            except Exception:
                pass
