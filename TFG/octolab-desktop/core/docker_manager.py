import os
import subprocess
import time
import docker
from config import (
    KALI_IMAGE, META_IMAGE,
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
_PORTS: dict[str, dict] = {
    META_CONTAINER: {"80/tcp": 8080},
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

    # ── Imágenes personalizadas ───────────────────────────────────────
    def _imagen_existe(self, imagen: str) -> bool:
        try:
            self.client.images.get(imagen)
            return True
        except (docker.errors.ImageNotFound, Exception):
            return False

    def _construir_imagen(self, tag: str, dockerfile: str,
                          on_status=None) -> bool:
        """Build genérico: construye `tag` usando `dockerfile` en DOCKER_DIR."""
        if on_status:
            on_status(f"Construyendo imagen {tag} (primera vez ~3-5 min)...")
        log.info(f"Iniciando build de {tag}...")
        try:
            proc = subprocess.Popen(
                [
                    "docker", "build",
                    "--no-cache",
                    "-t", tag,
                    "-f", os.path.join(DOCKER_DIR, dockerfile),
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
                if on_status and ("#" in line or "step" in line.lower()):
                    on_status(line[:50] + ("…" if len(line) > 50 else ""))
            proc.wait()
            if proc.returncode == 0 or self._imagen_existe(tag):
                log.info(f"Imagen {tag} construida correctamente.")
                return True
            log.error(f"Build {tag} falló con código {proc.returncode}")
            if on_status:
                on_status(f"Error: build {tag} falló (código {proc.returncode})")
            return False
        except FileNotFoundError:
            msg = "Docker CLI no encontrado en PATH"
            log.error(msg)
            if on_status:
                on_status(msg)
            return False
        except Exception as e:
            log.error(f"Error construyendo {tag}: {e}")
            if on_status:
                on_status(f"Error: {e}")
            return False

    def construir_imagen_kali(self, on_status=None) -> bool:
        """Construye octolab-kali:latest desde Dockerfile.kali."""
        return self._construir_imagen(KALI_IMAGE, "Dockerfile.kali", on_status)

    def construir_imagen_meta(self, on_status=None) -> bool:
        """Construye octolab-meta:latest desde Dockerfile.meta."""
        return self._construir_imagen(META_IMAGE, "Dockerfile.meta", on_status)

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

        # Construir imagen custom si no existe todavía
        if nombre == KALI_CONTAINER and not self._imagen_existe(KALI_IMAGE):
            if not self.construir_imagen_kali(on_status):
                return False
        elif nombre == META_CONTAINER and not self._imagen_existe(META_IMAGE):
            if not self.construir_imagen_meta(on_status):
                return False

        self.crear_red()

        caps = _CAPS.get(nombre, [])
        user = _USER.get(nombre, None)
        ports = _PORTS.get(nombre, {})

        try:
            # ── Comprobar si ya existe el contenedor ─────────────────
            try:
                c = self.client.containers.get(nombre)
                existing_caps = c.attrs.get("HostConfig", {}).get("CapAdd") or []
                existing_user = c.attrs.get("Config", {}).get("User", "")
                existing_ports = c.attrs.get("HostConfig", {}).get("PortBindings") or {}
                caps_ok = not caps or all(cap in existing_caps for cap in caps)
                user_ok = not user or existing_user == user
                ports_ok = not ports or all(p in existing_ports for p in ports)
                if not caps_ok or not user_ok or not ports_ok:
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
            if ports:
                run_kwargs["ports"] = ports

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
