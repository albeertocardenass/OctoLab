import subprocess
import time
import docker
from config import (
    KALI_IMAGE, METASPLOITABLE_IMAGE,
    KALI_CONTAINER, META_CONTAINER, DOCKER_NETWORK
)
from utils.logger import get_logger

log = get_logger("docker_manager")

class DockerManager:
    def __init__(self):
        self.client = None

    def iniciar_docker_desktop(self) -> bool:
        import platform
        if platform.system() != "Windows":
            return self._ping()

        subprocess.Popen(
            r"C:\Program Files\Docker\Docker\Docker Desktop.exe",
            shell=True
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
        """Intenta conectar con Docker si aún no hay cliente activo."""
        if self.client is not None:
            try:
                self.client.ping()
                return True
            except Exception:
                self.client = None
        return self._ping()

    def crear_red(self):
        """Crea la red interna para que Kali y Metasploitable se vean entre sí."""
        if not self._ensure_client():
            return
        try:
            self.client.networks.get(DOCKER_NETWORK)
        except docker.errors.NotFound:
            self.client.networks.create(DOCKER_NETWORK, driver="bridge")
            log.info(f"Red {DOCKER_NETWORK} creada.")

    def lanzar_contenedor(self, nombre: str, imagen: str) -> bool:
        if not self._ensure_client():
            log.error("Docker no disponible.")
            return False
        try:
            try:
                c = self.client.containers.get(nombre)
                if c.status != "running":
                    c.start()
                    log.info(f"{nombre} reanudado.")
                return True
            except docker.errors.NotFound:
                pass

            self.client.containers.run(
                imagen,
                name=nombre,
                network=DOCKER_NETWORK,   # Red NAT interna compartida
                detach=True,
                tty=True,
                stdin_open=True,
            )
            log.info(f"{nombre} lanzado en red {DOCKER_NETWORK}.")
            return True
        except Exception as e:
            log.error(f"Error lanzando {nombre}: {e}")
            return False

    def lanzar_labs(self, callback=None) -> bool:
        self.crear_red()
        ok_kali = self.lanzar_contenedor(KALI_CONTAINER, KALI_IMAGE)
        if callback:
            callback("Kali iniciado..." if ok_kali else "Error al iniciar Kali")
        ok_meta = self.lanzar_contenedor(META_CONTAINER, METASPLOITABLE_IMAGE)
        if callback:
            callback("Metasploitable iniciado..." if ok_meta else "Error al iniciar Metasploitable")
        return ok_kali and ok_meta

    def get_ip_contenedor(self, nombre: str) -> str | None:
        """Devuelve la IP del contenedor en la red interna octolab-net."""
        if not self._ensure_client():
            return None
        try:
            c = self.client.containers.get(nombre)
            redes = c.attrs.get("NetworkSettings", {}).get("Networks", {})
            ip = redes.get(DOCKER_NETWORK, {}).get("IPAddress")
            return ip or None
        except Exception:
            return None

    def exec_comando(self, contenedor: str, comando: str) -> str:
        try:
            c = self.client.containers.get(contenedor)
            result = c.exec_run(comando, tty=True)
            return result.output.decode(errors="replace")
        except Exception as e:
            return f"Error: {e}"

    def parar_labs(self):
        for nombre in [KALI_CONTAINER, META_CONTAINER]:
            try:
                self.client.containers.get(nombre).stop()
                log.info(f"{nombre} parado.")
            except Exception:
                pass

    def estado_contenedor(self, nombre: str) -> str:
        if not self._ensure_client():
            return "stopped"
        try:
            return self.client.containers.get(nombre).status
        except Exception:
            return "stopped"
