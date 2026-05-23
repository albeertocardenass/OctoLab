import requests
from config import API_LOGIN, API_VERIFY_CODE, API_PROGRESO
from utils.logger import get_logger

log = get_logger("api_client")

class ApiClient:
    def __init__(self):
        self.token: str | None = None

    def login(self, email: str, password: str) -> dict:
        try:
            r = requests.post(API_LOGIN, json={"email": email, "password": password}, timeout=10)
            r.raise_for_status()
            data = r.json()
            self.token = data.get("token")
            return {"ok": True, "data": data}
        except requests.exceptions.ConnectionError:
            return {"ok": False, "error": "No se puede conectar al servidor."}
        except requests.exceptions.HTTPError as e:
            return {"ok": False, "error": f"Credenciales incorrectas. ({e.response.status_code})"}
        except Exception as e:
            log.error(f"Login error: {e}")
            return {"ok": False, "error": str(e)}

    def verificar_codigo(self, usuario_id: int, tema_id: int, codigo: str) -> dict:
        try:
            r = requests.post(
                API_VERIFY_CODE,
                json={"usuarioId": usuario_id, "temaId": tema_id, "codigo": codigo},
                timeout=10
            )
            r.raise_for_status()
            return {"ok": True, "data": r.json()}
        except Exception as e:
            log.error(f"verificar_codigo error: {e}")
            return {"ok": False, "error": str(e)}

    def get_progreso(self, usuario_id: int) -> dict:
        try:
            r = requests.get(f"{API_PROGRESO}/{usuario_id}", timeout=10)
            r.raise_for_status()
            return {"ok": True, "data": r.json()}
        except Exception as e:
            log.error(f"get_progreso error: {e}")
            return {"ok": False, "error": str(e)}
